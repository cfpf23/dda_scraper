import datetime
import re
from pathlib import Path
from typing import List

import pandas as pd
import scrapy
from engines.playwright.playwright_engine import PlaywrightDriver
from functions.driver_functions.common_functions import (
    map_step_container,
    process_config_scenarios,
    process_config_scenarios_container,
    on_enter_every_time,
    on_enter_once,
    pagination,
)
from functions.driver_functions.rendering_driver_functions import driver_actions
from functions.parsing_functions.parsing_functions import mapping
from functions.utility_functions.decorators import run_once
from functions.utility_functions.utility_functions import (
    file_exists,
    file_exists_error,
    find_yaml_config,
    open_input_file,
    check_start_urls,
    save_to_csv,
    append_df_to_excel,
)
from yaml_interpreter.interpet import YamlInterpreter
# date_report = datetime.date.today().strftime("%Y-%m-%d")


class TurboContentPlaywright:
    date_report = datetime.date.today().strftime("%Y-%m-%d")
    output_columns = None

    def __init__(
        self,
        page_type,
        yaml_config_path,
        input_file_path=None,
        output_path=None,
        start_urls=None,
        input_file_sheet_name=0,
    ) -> None:
        self.yaml_config = find_yaml_config(page_type, yaml_config_path)
        self.on_enter_once_scenarios = self.yaml_config.get_on_enter_once_scenarios()
        self.on_enter_every_time_scenarios = self.yaml_config.get_on_enter_scraping_type_scenarios()
        if input_file_path:
            self.input_file_df = open_input_file(input_file_path, input_file_sheet_name)
        self.start_urls = check_start_urls(start_urls)
        self.output_path = output_path
        self.driver = PlaywrightDriver(headless=False, headers=self.yaml_config.headers)

    def start_requests(self):
        if self.start_urls:
            self.requests_url_list()
        else:
            self.requests_input_file()

    def update_item(self, item, new_values):
        item.update(new_values)

    def get_output_columns(self, additional_columns=None):
        config_file_columns = self.yaml_config.get_all_fields()
        if additional_columns:
            self.output_columns = config_file_columns + additional_columns
        else:
            self.output_columns = config_file_columns

    def save_item(self, item):
        if isinstance(item, List):
            item_dataframe = pd.DataFrame(item, columns=self.output_columns)
        else:
            item_dataframe = pd.DataFrame([item], columns=self.output_columns)

        if self.output_path.endswith(".csv"):
            save_to_csv(self.output_path, item_dataframe)
        else:
            append_df_to_excel(self.output_path, item_dataframe)

    def requests_url_list(self):
        additonal_output_columns = ["date"]
        self.get_output_columns(additonal_output_columns)

        fields_scenarios = self.yaml_config.get_fields_scenarios()
        for url in self.start_urls:
            additional_item_fields = {"date": self.date_report}
            self.driver.scrape(url)
            self.driver.wait(self.yaml_config.download_delay)
            on_enter_once(self.driver, self.on_enter_once_scenarios)
            on_enter_every_time(self.driver, self.on_enter_every_time_scenarios)
            item = process_config_scenarios(fields_scenarios, self.driver)
            self.update_item(item, additional_item_fields)
            self.save_item(item)

    def requests_input_file(self):
        additonal_output_columns = [
            "e_retailer",
            "client",
            "market",
            "type",
            "product_url",
            "keyword",
            "date",
        ]
        input_file_columns = ["e_retailer", "client", "market", "type", "product_url", "keyword"]
        self.get_output_columns(additonal_output_columns)
        content_template = self.input_file_df[input_file_columns].values.tolist()
        fields_scenarios = self.yaml_config.get_fields_scenarios()

        for e_retailer, client, market, type, product_url, keyword in content_template:
            additional_item_fields = {
                "date": self.date_report,
                "e_retailer": e_retailer,
                "client": client,
                "market": market,
                "type": type,
                "keyword": keyword,
            }
            self.driver.scrape(product_url)
            self.driver.wait(self.yaml_config.download_delay)
            on_enter_once(self.driver, self.on_enter_once_scenarios)
            on_enter_every_time(self.driver, self.on_enter_every_time_scenarios)
            item = process_config_scenarios(fields_scenarios, self.driver)
            self.update_item(item, additional_item_fields)
            self.save_item(item)


class TurboListingPlaywright:
    # date_report = datetime.date.today().strftime("%Y-%m-%d")
    output_columns = None
    page_limit = float("inf")

    def __init__(
        self,
        page_type,
        yaml_config_path,
        input_file_path=None,
        output_path=None,
        start_urls=None,
        input_file_sheet_name=0,
    ) -> None:
        self.yaml_config = find_yaml_config(page_type, yaml_config_path)
        self.on_enter_once_scenarios = self.yaml_config.get_on_enter_once_scenarios()
        self.on_enter_every_time_scenarios = self.yaml_config.get_on_enter_scraping_type_scenarios()
        self.pagination_scenarios = self.yaml_config.pagination
        if input_file_path:
            self.input_file_df = open_input_file(input_file_path, input_file_sheet_name)
        self.start_urls = check_start_urls(start_urls)
        self.output_path = output_path
        self.driver = PlaywrightDriver(**self.yaml_config.engine_settings)

    def get_output_columns(self, additional_columns=None):
        config_file_columns = self.yaml_config.get_all_fields_containers()
        if additional_columns:
            self.output_columns = config_file_columns + additional_columns
        else:
            self.output_columns = config_file_columns

    def save_item(self, item):
        if isinstance(item, List):
            item_dataframe = pd.DataFrame(item, columns=self.output_columns)
        else:
            item_dataframe = pd.DataFrame([item], columns=self.output_columns)

        if self.output_path.endswith(".csv"):
            save_to_csv(self.output_path, item_dataframe)
        else:
            append_df_to_excel(self.output_path, item_dataframe)

    def start_requests(self):
        if self.start_urls:
            self.requests_url_list()
        else:
            self.requests_input_file()

    def requests_url_list(self):
        additonal_columns = ["position", "listing_url", "date"]
        self.get_output_columns(additonal_columns)

        containers = self.yaml_config.get_all_container_scenarios()
        for url in self.start_urls:
            self.driver.scrape(url)
            on_enter_once(self.driver, self.on_enter_once_scenarios)
            on_enter_every_time(self.driver, self.on_enter_every_time_scenarios)
            page = 1
            while True:
                additional_item_fields = {"date": self.date_report, "page": page}
                if containers:
                    item_container = self.handle_containers(containers)
                    self.update_item(item_container, additional_item_fields)
                    self.save_item(item_container)
                if page >= self.page_limit or not pagination(self.driver, self.pagination_scenarios):
                    break
                page += 1

    def update_item(self, item_container, new_values):
        for item in item_container:
            item.update(new_values)

    def requests_input_file(self):
        additonal_output_columns = [
            "e_retailer",
            "client",
            "market",
            "type",
            "position",
            "listing_url",
            "page",
            "date",
        ]
        input_file_columns = ["e_retailer", "client", "market", "type", "listing_link", "pages", "keyword"]
        self.get_output_columns(additonal_output_columns)
        listing_template = self.input_file_df[input_file_columns].values.tolist()

        containers = self.yaml_config.get_all_container_scenarios()
        for e_retailer, client, market, type, listing_link, pages, keyword in listing_template:
            self.page_limit = pages
            self.driver.scrape(listing_link)
            self.driver.wait(self.yaml_config.download_delay)
            on_enter_once(self.driver, self.on_enter_once_scenarios)
            on_enter_every_time(self.driver, self.on_enter_every_time_scenarios)
            page = 1
            while True:
                additional_item_fields = {
                    "date": self.date_report,
                    "e_retailer": e_retailer,
                    "client": client,
                    "market": market,
                    "type": type,
                    "keyword": keyword,
                    "page": page,
                }
                if containers:
                    item_container = self.handle_containers(containers)
                    self.update_item(item_container, additional_item_fields)
                    self.save_item(item_container)
                if page >= self.page_limit or not pagination(self.driver, self.pagination_scenarios):
                    break
                page += 1

    def handle_containers(self, containers):
        dataset = []
        for container in containers:
            parent_selector = container.get("parent_selector")
            container_fields = container.get("fields")
            child_selectors = self.driver.get_child_selectors(parent_selector)
            for position, child_selector in enumerate(child_selectors, 1):
                item = {"position": position, "listing_url": self.driver.current_url}
                fields_scenarios = self.yaml_config.get_fields_scenarios_container(container_fields)
                item.update(process_config_scenarios_container(fields_scenarios, self.driver, child_selector))
                dataset.append(item)

        return dataset

