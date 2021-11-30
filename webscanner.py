import logging
import re
import sys
from urllib.parse import urlparse

import click
import requests


class WebScanner:
    """WebCrawler class to automatically find broken links and other issues with a website.

    Args:
        url (string): The url to start crawling.
        prefix (string, optional): Everything with a different prefix is treated as external.
            This allows for limiting the crawler to a subdirectory. Defaults to None.
        max_depth (integer, optional): Maximum crawl depth, None is unlimited. Defaults to None.
        test_external_urls (bool, optional): Test the status code of external links or not. Defaults to False.
        headers (dict, optional): Custom headers dictionary for example to provide login details. Defaults to None.
        verbose (int, optional): How much we output, should be 0,1 or 2. At level 0 only broken links are reported. Defaults to 0.
    """

    visited_links = []
    logger = None
    exit_code = 0

    def __init__(
        self,
        url,
        prefix=None,
        max_depth=None,
        test_external_urls=False,
        headers=None,
        verbose=0,
    ):
        self.logger = logging.getLogger("crawler")
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s - %(message)s")
        c_handler.setFormatter(fmt)
        self.logger.addHandler(c_handler)
        # use a session
        self.session = requests.Session()

        parsed_url = urlparse(url)
        self.root_url = parsed_url.scheme + "://" + parsed_url.netloc
        self.prefix = prefix
        if prefix == None:
            self.prefix = self.root_url
        self.host = parsed_url.netloc
        self.verbose = verbose
        self.max_depth = max_depth
        self.start_url = url
        self.test_external_urls = test_external_urls
        if headers:
            self.session.headers.update(headers)
        else:
            # standard headers for emulating chrome
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Dnt": "1",
                "Host": self.host,
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            }
            self.session.headers.update(headers)

    def crawl(self, current_link=None, depth=0):
        """Crawl through the documentation page and return the status code of the links.

        Keep track of visited links. When a new link is visited request its HTML and get all anchors found in it.
        If they are external links, return their status code. If they are internal and they are relative paths,
        make them first complete and then return their status.

        For every link visited go deeper and deeper to visit all links found in it.

        Args:
            current_link (string, optional): The current link to download and crawl (if not visited yet). Defaults to None.
            depth (int, optional): The current recursive depth. Defaults to 0.
        """        
        if current_link == None:
            current_link = self.start_url
        if depth > self.max_depth:
            return
        if current_link in self.visited_links:
            return

        res = self.session.get(current_link)

        self.visited_links.append(current_link)
        if self.verbose == 2:
            self.logger.info(f"{current_link}\t{res.status_code}")
        if self.verbose == 1:
            print("#", end="", flush=True)

        if not res.ok:
            self.exit_code += 1
            self.logger.error(f"{current_link} returned a {res.status_code}")
            return

        urls = re.findall(r'href=[\'"]?([^\'" >]+)', res.text)

        for link in urls:
            # remove query part and anchors
            link = self.clean_url(link)
            if not self.is_external(link):
                if link.startswith("/"):
                    link = self.root_url + link
                elif not link.startswith("http"):
                    link = current_link + link
                self.crawl(link, depth + 1)
            elif self.test_external_urls:
                external_res = requests.get(link)
                if not external_res.ok:
                    self.logger.warning(
                        f"External Page: {link} returned a {external_res.status_code}"
                    )
                    return

    def clean_url(self, url):
        """Remove the query and anchors from a url.

        Args:
            url (string): Url to clean.

        Returns:
            string: url without anchors and query parameters.
        """        
        url = url.split("?")[0]  # remove any querystrings
        return url.split("#")[0]  # remove any anchors

    def is_external(self, url):
        """Check if url is in the part we want to crawl.

        Args:
            url (string): The url to check.

        Returns:
            bool: boolean indicating whether we treat the url as external or not.
        """ 
        if not url.startswith("http") or url.startswith(self.prefix):
            return False
        return True


@click.command()
@click.argument("url", required=True)
@click.option(
    "--prefix",
    "-p",
    default=None,
    help="A prefix to prevent the crawler from accessing top dirs.",
)
@click.option(
    "--max_depth",
    "-d",
    default=None,
    type=int,
    help="The maximum recursive depth to crawl.",
)
@click.option(
    "--test_external_urls",
    "-e",
    default=False,
    type=bool,
    help="Whether to test external urls or not.",
)
@click.option(
    "--verbose",
    "-v",
    default=0,
    type=int,
    help="Either 0,1 or 2. Controls how much output is generated.",
)
def cli(url, prefix, max_depth, test_external_urls, verbose):
    crawler = WebScanner(
        url,
        prefix=prefix,
        max_depth=max_depth,
        test_external_urls=test_external_urls,
        verbose=verbose,
    )
    crawler.crawl()
    # give the exit code (handy for pipeline checks etc.)
    # the exit_code is the number of broken links found
    sys.exit(crawler.exit_code)


if __name__ == "__main__":
    cli()
