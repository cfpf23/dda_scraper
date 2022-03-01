"""
This module offers a functionality which allows a person to call multiple spiders sequentially through scrapy API
without the usage of command line
"""

import pandas as pd
from e_retailer_scraper.spiders.pl import TurboContentPlaywright, TurboListingPlaywright
from e_retailer_scraper.spiders.generic_scrapy import TurboContentScrapy, TurboListingScrapy
from e_retailer_scraper.spiders.generic_scrapy import run_scrapy_spider
from e_retailer_scraper.turbo_spider import TurboContent


def content():

    urls = [
        "https://www.mediamarkt.de/de/product/_braun-9465cc-wetanddry-rasierer-grau-active-quattro-head-2752175.html",
        "https://www.mediamarkt.de/de/product/_oral-b-io-7-mit-magnet-technologie-sanften-mikrovibrationen-2752152.html",
        "https://www.mediamarkt.de/de/product/_braun-9410s-rasierer-schwarz-active-quattro-head-2752174.html",
    ]
    turbo_content = TurboContentPlaywright(
        page_type="listing",
        yaml_config_path="C:/Users/Olaf/Desktop/spider_template/e_retailer_library/mediamarkt_de.yaml",
        start_urls=urls,
        output_path="jazda.csv",
    )
    turbo_content.start_requests()


def listing():
    # urls = ["https://www.elgiganten.dk/search/ipl"]
    input_file = "/input/listing/listing_template_elgiganten.dk.xlsx"
    turbo_listing = TurboListingPlaywright(
        page_type="listing",
        yaml_config_path="/e_retailer_library/elgiganten_dk.yaml",
        # start_urls=urls,
        input_file_path=input_file,
        output_path="elgiganten_dk.csv",
    )
    turbo_listing.start_requests()


def scrapy_run():
    # urls = [
    #     "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
    #     "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    #     "https://books.toscrape.com/catalogue/soumission_998/index.html",
    #     "https://books.toscrape.com/catalogue/sharp-objects_997/index.html",
    #     "https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html",
    #     "https://books.toscrape.com/catalogue/the-requiem-red_995/index.html",
    #     "https://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html",
    #     "https://books.toscrape.com/catalogue/the-coming-woman-a-novel-based-on-the-life-of-the-infamous-feminist-victoria-woodhull_993/index.html",
    # ]
    input_file = "/input/listing/listing_template_amazon.xlsx"
    run_scrapy_spider(
        TurboListingScrapy,
        page_type="listing",
        yaml_config_path="/e_retailer_library/amazon_scrapy.yaml",
        # start_urls=urls,
        input_file_path=input_file,
    )


# content()
listing()
# scrapy_run()
