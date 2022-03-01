from e_retailer_scraper.spiders.generic_scrapy import TurboContentScrapy, TurboListingScrapy
from e_retailer_scraper.spiders.pl import TurboContentPlaywright, TurboListingPlaywright
from functions.utility_functions.utility_functions import find_yaml_config
from scrapy.crawler import CrawlerProcess
import scrapy


class TurboContent:
    def __init__(self, driver_type, page_type, yaml_config_path, input_file_path=None, output_path=None, start_urls=None, spider_name="turbo_pdp"):
        self.yaml_config = find_yaml_config(page_type, yaml_config_path)
        self.yaml_config_path = yaml_config_path
        self.engine = self.find_engine(driver_type, page_type)
        print(self.engine)
        self.output_path = output_path
        self.input_file_path = input_file_path
        self.driver_type = driver_type
        self.page_type = page_type
        self.spider_name = spider_name
        self.start_urls = start_urls

    def find_engine(self, driver_type: str, page_type: str):
        engines = {
            ("scrapy", "product_card"): TurboContentScrapy,
            ("playwright", "product_card"): TurboContentPlaywright,
        }
        try:
            return engines[(driver_type, page_type)]
        except KeyError:
            raise KeyError("Driver or page type is not supported")

    def start_scraping(self):
        if self.engine == TurboContentScrapy:
            process = CrawlerProcess(settings=self.yaml_config.engine_settings)
            process.crawl(self.engine, name=self.spider_name, page_type=self.page_type, yaml_config_path=self.yaml_config_path, start_urls=self.start_urls)
            process.start()
        # if isinstance(self.engine, TurboContentPlaywright):
        #     turbo_content = self.engine(
        #         page_type=self.page_type,
        #         yaml_config_path=self.yaml_config_path,
        #         start_urls=self.start_urls,
        #         output_path=self.output_path
        #     )
        #     turbo_content.start_requests()


class TurboListing:
    def __init__(self, driver_type, page_type, yaml_config_path, input_file_path=None, output_path=None, start_urls=None, spider_name="turbo_listing"):
        self.yaml_config = find_yaml_config(page_type, yaml_config_path)
        self.yaml_config_path = yaml_config_path
        self.engine = self.find_engine(driver_type, page_type)
        self.output_path = output_path
        self.input_file_path = input_file_path
        self.driver_type = driver_type
        self.page_type = page_type
        self.spider_name = spider_name

    def find_engine(self, driver_type: str, page_type: str):
        engines = {
            ("scrapy", "listing"): TurboListingScrapy,
            ("playwright", "listing"): TurboListingPlaywright,
        }
        try:
            return engines[(driver_type, page_type)]
        except KeyError:
            raise KeyError("Driver or page type is not supported")

    def start_scraping(self):
        if isinstance(self.engine, TurboListingScrapy):
            process = CrawlerProcess(settings=self.yaml_config.engine_settings)
            process.crawl(self.engine, name=self.spider_name, page_type=self.page_type, yaml_config_path=self.yaml_config_path, start_urls=self.start_urls)
            process.start()
        if isinstance(self.engine, TurboListingPlaywright):
            turbo_content = self.engine(
                page_type=self.page_type,
                yaml_config_path=self.yaml_config_path,
                start_urls=self.start_urls,
                output_path=self.output_path
            )
            turbo_content.start_requests()