# Spider Template

This project allows user to create Playwright or Scrapy spiders with the same inferface via creating **.yaml** templates for any website (almost) user wants to scrape.

## Installation

Be sure to create custom .env with either venv/conda/poetry etc

### Pre-requisite

```bash
  Python >= 3.8
```

```bash
  pip install requirements.txt
  playwright install # Playwright's browsers binaries
```

## Templates

### Default Scrapy template:

```yaml
info:
  name: #e-retailer name
  domain: #e-retailer domain
  country: #country domain extension
  product_card_examples: []
  listing_examples: []
  warnings: []

options:
  scrape_options:
   engine: scrapy
   # engine setting are the same as with normal settings.py file for scrapy, more on that:
   # https://docs.scrapy.org/en/latest/topics/settings.html
   engine_settings:
    DEFAULT_REQUEST_HEADERS:
        referer: https://google.com
        pragma: no-cache
        cache-control: no-cache
        rtt: '600'
        downlink: '1.5'
        ect: 3g
        dnt: '1'
        upgrade-insecure-requests: '1'
        accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        sec-fetch-site: same-origin
        sec-fetch-mode: navigate
        sec-fetch-user: "?1"
        sec-fetch-dest: document
        accept-language: en-US,en;q=0.9,ur;q=0.8,zh-CN;q=0.7,zh;q=0.6
        accept-Encoding: gzip, deflate, br
    USER_AGENT: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ROBOTSTXT_OBEY: False
    DOWNLOAD_DELAY: 0.2
    DOWNLOAD_TIMEOUT: 30
    CONCURRENT_REQUESTS_PER_DOMAIN: 20
    COOKIES_ENABLED: False
    DOWNLOADER_MIDDLEWARES:
        scrapy.downloadermiddlewares.useragent.UserAgentMiddleware: null
        scrapy.downloadermiddlewares.retry.RetryMiddleware: null
        scrapy_fake_useragent.middleware.RandomUserAgentMiddleware: 400
        scrapy_fake_useragent.middleware.RetryUserAgentMiddleware: 401
    FAKEUSERAGENT_PROVIDERS:
        - scrapy_fake_useragent.providers.FakeUserAgentProvider
        - scrapy_fake_useragent.providers.FakerProvider
        - scrapy_fake_useragent.providers.FixedUserAgentProvider  # fall back to USER_AGENT value
    AUTOTHROTTLE_ENABLED: True
    AUTOTHROTTLE_START_DELAY: 5.0
    AUTOTHROTTLE_MAX_DELAY: 60.0
    AUTOTHROTTLE_TARGET_CONCURRENCY: 10.0
    AUTOTHROTTLE_DEBUG: False
    RETRY_ENABLED: True
    RETRY_TIMES: 4
    RETRY_HTTP_CODES: [500,502,503,504,400,401,403,404,405,406,407,408,409,410,429]
    FEEDS:
      "generic_listing.csv": {"format": "csv"}
    LOG_FILE: "logs/generic_listing.log"

product_card:

  fields:

    field_name:
      scenarios:
        - - get_element: {css: }
            parsing_functions: {}

    field_name:
      scenarios:
        - - get_elements: {css: }
            parsing_functions:
                input: {strip: } # [str.strip(), str.strip(), str.strip()]
                output: {join: ","} # ",".join([])


listing:

  containers:
  - parent_selector: #parent selector containing multiple fields that we want to scrape
    page_type: # search/category/review
    fields:

        field_name:
        scenarios:
            - - get_element: {css: }
                parsing_functions: {}

        field_name:
        scenarios:
            - - get_elements: {css: }
                parsing_functions:
                    input: {strip: } # [str.strip(), str.strip(), str.strip()]
                    output: {join: ","} # ",".join([])

  pagination:
    scenarios:
      - - go_to: {css: , attr: }
```

### Default Playwright template:

```yaml
info:
  name: #e-retailer name
  domain: #e-retailer domain
  country: #country domain extension
  product_card_examples: []
  listing_examples: []
  warnings: []

options:
  scrape_options:
    engine: playwright
    engine_settings:
      # start in headless?
      headless:
      # headers for each request
      headers:
        Pragma: no-cache
        Cache-control: no-cache
        Upgrade-insecure-requests: '1'
        Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
        Sec-fetch-site: same-origin
        Sec-fetch-mode: navigate
        Sec-fetch-user: "?1"
        Sec-fetch-dest: document
        Accept-language: en-US,en;q=0.9,ur;q=0.8,zh-CN;q=0.7,zh;q=0.6
        Accept-Encoding: gzip, deflate, br
      # default browser arguments loaded at the engine start
      args:
        -
        -
        -
      # set proxy credentials if needed
      proxy_address:
        server: "http://proxy_server:proxy_port"
        username: username
        password: password
      # user agent set for every request
      user_agent:
      # viewport of browser window
      viewport: {"width": , "height": }
      # reosource to block while sending a request
      route_block:


# this on_enter handles driver actions only once at the beggining of scraping
# example: clicking cookies
on_enter:
  scenarios:



product_card:

  options:
    # Arbitrary time to wait after entering each page
    download_delay:

  # this on_enter handles driver actions every time page is scraped
  # example: scrolling down to load more products
  on_enter:
    scenarios:


  fields:

    field_name:
      scenarios:
        - - get_element: {css: }
            parsing_functions: {}

    field_name:
      scenarios:
        - - get_elements: {css: }
            parsing_functions:
                input: {strip: } # [str.strip(), str.strip(), str.strip()]
                output: {join: ","} # ",".join([])

listing:

  options:
    # Arbitrary time to wait after entering each page
    download_delay:

  # this on_enter handles driver actions every time page is scraped
  # example: scrolling down to load more products
  on_enter:
    scenarios:



  containers:
  - parent_selector: #parent selector containing multiple fields that we want to scrape
    page_type: # search/category/review
    fields:
        field_name:
          scenarios:
              - - get_element: {css: }
                  parsing_functions: {}

        field_name:
          scenarios:
              - - get_elements: {css: }
                  parsing_functions:
                    input: {strip: } # [str.strip(), str.strip(), str.strip()]
                    output: {join: ","} # ",".join([])


  # pagination handling
  pagination:
    scenarios:
      - - go_to: {css: , attr: } # use this one if there is a link for the next page
      - - pagination_click: {css: } # use this one if pagination is handled by js button

```

### Playwright template misc

You can any driver action as a step in between get_element/get_elements if for example there is a need to click something to load the data:

```yaml
field_name:
  scenarios:
    - - click: { css }
      - get_elements: { css }
        parsing_functions:
          input: { strip }
          output: { join: "," }
```

### Common usage in Templates

Both **get_element** and **get_elements** can have additional arguments passed if neeeded:

- attr

```bash
   #If one needs to extract attribute of a selector
   get_elements: {css: , attr:}
```

- re

```bash
   #If the value one is looking for is nested in script tag, or overall usage of regex in needed
   get_elements: {css: , re:}
```

If css may vary between different urls you can define more than one scenario, and framework will take whichever is present:

```yaml
field_name:
  scenarios:
    - - get_element: { css }
      - parsing_functions: {}

    - - get_element: { css }
      - parsing_functions: {}
```

## Driver actions

At the moment the possible actions with the renering engine are:

```bash
- click: {css: , optional: } # click at the selector, can be optional. Not optional by defaulut
- click_postion: {x: , y:}   # click at the position x, y
- pagination_click: {css: }  # click at the selector, used only for pagination
- move: {x: , y:}            # move mouse to the position x, y
- wait: {seconds: }          # wait arbitrary time in seconds
- scroll: {x: , y:}          # scroll mouse wheel to the position x, y
- go_to: {css: attr:}        # redirect to the next page by attr
- solve_amazon_captcha: {}   # solve existing amazon captcha
- infinite_scroll: {}        # scroll infinitely until no more products are loaded
- hover_on: {css: }          # hover mouse cursor over css element
- focus_on: {css:}           # driver will try to find css element and afterwards focus on it

```

To add new driver action you need to create a new method in **playwright_engine.py** and afterwards add new key in **rendering_driver_functions.py**:

```bash
mapping = {
    "click": driver.click,
    "click_postion": driver.click_position,
    "pagination_click": driver.pagination_click,
    "move": driver.move,
    "wait": driver.wait,
    "scroll": driver.scroll,
    "go_to": driver.go_to,
    "solve_amazon_captcha": driver.solve_amazon_captcha,
    "infinite_scroll": driver.infinite_scroll,
    "focus_on": driver.focus_on,
    "hover_on": driver.hover_on,
}
```

## Usage

To use this framework you need to either use spiders provided by default in directory **e_retailer_scraper/spiders/** or create a new custom spiders based on the default ones, afterwards just create a **.py** file which will handle running the framework (run.py by default) and import spiders which you want to run

## Playwright Spiders:

### Listing

```bash
input_file = "/input/listing/listing_template_elgiganten.dk.xlsx" # file with the input scope
start_urls = []                                                   # list of urls if there is not any input file
turbo_listing = TurboListingPlaywright(
    page_type="listing",                                          # type of scraping taken from the .yaml file
    yaml_config_path="/e_retailer_library/elgiganten_dk.yaml",    # .yaml file with configuration
    # start_urls=urls,                                            # list of urls to scrape if any
    input_file_path=input_file,                                   # path to input file with the scope
    input_file_sheet_name="",                                      # input file sheet name
    output_path="elgiganten_dk.csv",                              # output file path

)
turbo_listing.start_requests()                                    # start scraping
```

### Product card

```bash
input_file = "/input/listing/listing_template_elgiganten.dk.xlsx" # file with the input scope
start_urls = []                                                   # list of urls if there is not any input file
turbo_content = TurboConetnPlaywright(
    page_type="product_card",                                     # type of scraping taken from the .yaml file
    yaml_config_path="/e_retailer_library/elgiganten_dk.yaml",    # .yaml file with configuration
    # start_urls=urls,                                            # list of urls to scrape if any
    input_file_path=input_file,                                   # path to input file with the scope
    input_file_sheet_name="",                                      # input file sheet name
    output_path="elgiganten_dk.csv",                              # output file path
)
turbo_content.start_requests()                                    # start scraping
```

## Scrapy Spiders:

### Listing

```bash
input_file = "/input/listing/listing_template_amazon.xlsx"       # file with the input scope
start_urls = []                                                  # list of urls if there is not any input file
run_scrapy_spider(
    TurboListingScrapy,                                          # Scrapy spider class name
    page_type="listing",                                         # type of scraping taken from the .yaml file
    yaml_config_path="/e_retailer_library/amazon_scrapy.yaml",   # .yaml file with configuration
    # start_urls=urls,                                           # list of urls to scrape if any
    input_file_path=input_file,                                  # path to input file with the scope
    input_file_sheet_name=""                                     # input file sheet name
)
```

### Product card

```bash
input_file = "/input/listing/listing_template_amazon.xlsx"       # file with the input scope
start_urls = []                                                  # list of urls if there is not any input file
run_scrapy_spider(
    TurboContentScrapy,                                          # Scrapy spider class name
    page_type="product_card",                                    # type of scraping taken from the .yaml file
    yaml_config_path="/e_retailer_library/amazon_scrapy.yaml",   # .yaml file with configuration
    # start_urls=urls,                                           # list of urls to scrape if any
    input_file_path=input_file,                                  # path to input file with the scope
)
```

Afterwards just run your file with command:

```bash
python run.py
```

## Authors

- [@Olaf Nowicki](https://github.com/onpf23)

## Special thanks:

**.yaml** Configuration are files based on **.json** implementation of:

- [@Piotr Sowiński](https://github.com/pspf23)

The man who first belived that Scrapy and renering frameworks can live in peace and harmony:

- [@Christian Ferrão](https://github.com/cfpf23)
