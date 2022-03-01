import datetime
import json
from typing import List, Union

import pandas as pd
import scrapy
from engines.scrapy.scrapy_engine import ScrapyEngine
from functions.driver_functions.common_functions import (
    map_step_container, pagination, process_config_scenarios,
    process_config_scenarios_container)
from functions.driver_functions.curl_driver_functions import driver_actions
from functions.parsing_functions.parsing_functions import mapping
from functions.utility_functions.decorators import run_once
from functions.utility_functions.utility_functions import (file_exists,
                                                           file_exists_error,
                                                           find_yaml_config,
                                                           open_input_file)
from scrapy.crawler import CrawlerProcess
from scrapy.http.response.html import HtmlResponse


class TurboListingScrapy(scrapy.Spider):

    date_report = datetime.date.today().strftime("%Y-%m-%d")

    def __init__(self, page_type: str, yaml_config_path:str , name: str = None, input_file_path: str = None, start_urls: List[str] = None, **kwargs: Union[str, int]):
        super().__init__(name=name, start_urls=start_urls, **kwargs)
        self.yaml_config = find_yaml_config(page_type, yaml_config_path)
        self.pagination_scenarios = self.yaml_config.pagination
        if input_file_path:
            self.input_file_df = open_input_file(input_file_path)

    def start_requests(self):
        if self.start_urls:
            current_page = 0
            page_limit = float("inf")
            for url in self.start_urls:
                yield scrapy.Request(
                    url=url,
                    cb_kwargs=dict(
                    page_limit=page_limit,
                    current_page=current_page,
                    )
                )
        else:
            current_page = 0
            input_file_columns = ["e_retailer", "client", "market", "type", "listing_link", "keyword", "pages"]
            listing_template = self.input_file_df[input_file_columns].values.tolist()
            for e_retailer, client, market, type, listing_link, keyword, pages in listing_template:
                yield scrapy.Request(
                    url=listing_link,
                    cb_kwargs=dict(
                        date=self.date_report,
                        page_limit=pages,
                        current_page=current_page,
                        e_retailer=e_retailer,
                        client=client,
                        market=market,
                        type=type,
                        keyword=keyword
                        )
                    )


    def parse(self, response: HtmlResponse, **cb_kwargs: Union[str, int]):
        driver = ScrapyEngine(response)
        containers = self.yaml_config.get_all_container_scenarios()
        if containers:
            yield from self.handle_containers(driver, containers, response)

        next_page = pagination(driver, self.pagination_scenarios)
        if next_page and (response.cb_kwargs["current_page"] < response.cb_kwargs["page_limit"]):
            yield response.follow(next_page, callback=self.parse, cb_kwargs=response.cb_kwargs)

    def handle_containers(self, driver: ScrapyEngine, containers: List[dict], response: HtmlResponse):
        response.cb_kwargs["current_page"] += 1
        for container in containers:
            parent_selector = container.get("parent_selector")
            container_fields = container.get("fields")
            child_selectors = driver.get_child_selectors(parent_selector)
            for position, child_selector in enumerate(child_selectors, 1):
                item = {"position": position, "listing_url": driver.current_url}
                if response.cb_kwargs:
                    item.update(response.cb_kwargs)
                fields_scenarios = self.yaml_config.get_fields_scenarios_container(container_fields)
                item.update(process_config_scenarios_container(fields_scenarios, driver, child_selector))
                yield item

class TurboContentScrapy(scrapy.Spider):

    date_report = datetime.date.today().strftime("%Y-%m-%d")
    def __init__(self, page_type: str, yaml_config_path:str , name: str = None, input_file_path: str = None, start_urls: List[str] = None, **kwargs: Union[str, int]):
        super().__init__(name=name, start_urls=start_urls, **kwargs)
        self.yaml_config = find_yaml_config(page_type, yaml_config_path)
        if input_file_path:
            self.input_file_df = open_input_file(input_file_path)

    def start_requests(self):
        if self.start_urls:
            for url in self.start_urls:
                yield scrapy.Request(
                    url=url,
                    cb_kwargs=dict()
                )
        else:
            input_file_columns = ["e_retailer", "client", "market", "type", "product_link", "keyword"]
            content_template = self.input_file_df[input_file_columns].values.tolist()
            for e_retailer, client, market, type, product_url, keyword in content_template:
                yield scrapy.Request(
                    url=product_url,
                    cb_kwargs=dict(
                        date=self.date_report,
                        e_retailer=e_retailer,
                        client=client,
                        market=market,
                        type=type,
                        keyword=keyword
                    )
                    )

    def parse(self, response: HtmlResponse, **cb_kwargs: Union[str, int]):
        driver = ScrapyEngine(response)
        fields_scenarios = self.yaml_config.get_fields_scenarios()
        item = {}
        if cb_kwargs:
            print(cb_kwargs)
            item.update(cb_kwargs)
        item.update(process_config_scenarios(fields_scenarios, driver))
        yield item



def run_scrapy_spider(scrapy_spider_class, page_type, yaml_config_path, input_file_path=None, start_urls=None, name="scrapy_spider"):
    yaml_config = find_yaml_config(page_type, yaml_config_path)
    process = CrawlerProcess(settings=yaml_config.engine_settings)
    process.crawl(scrapy_spider_class, name=name, page_type=page_type, yaml_config_path=yaml_config_path, start_urls=start_urls, input_file_path=input_file_path)
    process.start()


if __name__ == "__main__":
    run_scrapy_spider()
