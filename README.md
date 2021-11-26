# WebScanner

A simple crawler to detect broken links in websites.

![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## How to use

You can use and extend the tool to easily crawl a website and check for broken links and other errors.  
Download the pageCrawler.py and call it from the terminal using:

    python3 pageCrawler.py URL_TO_CRAWL

Check out all the options using

    python3 pageCrawler.py --help

You can also use the class directly in your own python code:

    crawler = WebCrawler(
        URL_TO_CRAWL,
        prefix=OPTIONAL_PREFIX,
        max_depth=2,
        test_external_urls=True,
        verbose=2,
    )
    crawler.crawl()

The *prefix* determines which links are crawled, for example you can limit the crawling to a specific subdirectory of a
domain such as https://domain.com/dir/
Everything above the /dir/ will be ignored, when setting the prefix to this url.

The *max_depth* determines how deep the crawler goes, for example if set to 1, only the links of the initial page are
followed and the process stops. If set to 2, all links of the initial page and all following links from the pages that
follow the initial page are crawled.

## Further development
1. Clone this repository
    ```bash
   git@github.com:F3licity/WebScanner.git
    ```
2. Start a new virtual environment on the root folder of this project, using Python 3.8, and activate it.
   ```bash
   pip3.8 install virtualenv
   virtualenv venv38
   source venv38/bin/activate
   ```
3. Install `pip` and [`pip-tools`]((https://github.com/jazzband/pip-tools)).
4. Install the pip libraries required:
   ```bash
   pip install -r requirements.txt
   ```
   
Start developing!