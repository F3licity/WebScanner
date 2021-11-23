import logging
import re
import requests
from urllib.parse import urlparse


class WebCrawler:
    """Crawl through a website and return broken links."""

    visited_links = []
    logger = None

    def __init__(self, url, max_depth = None, test_external_urls = False, headers=None, verbose=0):
        self.logger = logging.getLogger("crawler")
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s - %(message)s")
        c_handler.setFormatter(fmt)
        self.logger.addHandler(c_handler)
        #use a session
        self.session = requests.Session()

        parsed_url = urlparse(url)
        self.root_url = parsed_url.scheme + "://" + parsed_url.netloc
        self.host = parsed_url.netloc
        self.verbose = verbose
        self.max_depth = max_depth
        self.start_url = url
        if headers:
            self.session.headers.update(headers)
        else:
            #standard headers for emulating chrome
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

        :param current_link: Check whether the current link is already visited or not.
        :return: When done, exit the execution. Do not return anything.
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
            print("#", end = '')

        if not res.ok:
            self.logger.error(f"{current_link} returned a {res.status_code}")
            return

        urls = re.findall(r'href=[\'"]?([^\'" >]+)', res.text)

        for link in urls:
            #remove query part and anchors
            link = self.clean_url(link)
            if not link.startswith("http"):
                if link.startswith("/"):
                    link = self.root_url + link
                else:
                    link = current_link + link
                self.crawl(link, depth + 1)
            elif self.test_external_urls:
                external_res = self.session.get(link)
                if not external_res.ok:
                    self.logger.warning(
                        f"External Page: {link} returned a {external_res.status_code}"
                    )
                    return

    def clean_url(url):
        """Remove the query and anchors from a url.

        :param url: The url to clean.
        :return: the cleaned url.
        """
        url = url[:url.find('?')] #remove any querystrings
        return url[:url.find('#')] #remove any anchors

if __name__ == "__main__":
    crawler = WebCrawler("https://emerald-it.nl/", max_depth=2, test_external_urls=True, verbose=2)
    crawler.crawl()
