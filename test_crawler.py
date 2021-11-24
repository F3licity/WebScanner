import unittest

from pageCrawler import WebCrawler


class test_crawler(unittest.TestCase):
    def test_clean_url(self):
        crawler = WebCrawler("https://google.com/")
        newurl = crawler.clean_url("https://google.com/#everythingHereShouldBe#Removed")
        assert newurl == "https://google.com/"
        newurl = crawler.clean_url(
            "https://google.com/?a=everythingHereShouldBe#Removed"
        )
        assert newurl == "https://google.com/"

    def test_is_external(self):
        crawler = WebCrawler("https://google.com/")
        assert crawler.is_external("https://external.com/")
        assert not crawler.is_external("https://google.com/bla")

    def test_end_to_end(self):
        crawler = WebCrawler(
            "https://emerald-it.nl/",
            max_depth=1,
            test_external_urls=False,
            verbose=0,
        )
        crawler.crawl()


if __name__ == "__main__":
    unittest.main()
