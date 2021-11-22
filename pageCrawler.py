import logging
import re

import requests

MAIN_URL = ""


class DocumentationCrawler:
    """Crawl through the documentation page and return the status code of the links."""

    visited_links = []
    logger = None

    def __init__(self):
        self.logger = logging.getLogger("crawler")
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s - %(message)s")
        c_handler.setFormatter(fmt)
        self.logger.addHandler(c_handler)

    def crawl(self, current_link):
        """Crawl through the documentation page and return the status code of the links.

        Keep track of visited links. When a new link is visited request its HTML and get all anchors found in it.
        If they are external links, return their status code. If they are internal and they are relative paths,
        make them first complete and then return their status.

        For every link visited go deeper and deeper to visit all links found in it.

        :param current_link: Check whether the current link is already visited or not.
        :return: When done, exit the execution. Do not return anything.
        """
        if current_link in self.visited_links:
            return

        res = requests.get(current_link)

        self.visited_links.append(current_link)
        self.logger.warning(f"{current_link}\t{res.status_code}")
        if not res.ok:
            self.logger.error(f"{current_link} returned a {res.status_code}")
            return

        urls = re.findall(r'href=[\'"]?([^\'" >]+)', res.text)

        for link in urls:

            if not link.startswith("http"):
                if link.startswith("/"):
                    link = MAIN_URL + link
                else:
                    link = current_link + link
                self.crawl(link)
            else:
                external_res = requests.get(link)
                if not external_res.ok:
                    self.logger.warning(
                        f"External Page: {link} returned a {external_res.status_code}"
                    )
                    return


if __name__ == "__main__":
    crawler = DocumentationCrawler()
    crawler.crawl(MAIN_URL)
