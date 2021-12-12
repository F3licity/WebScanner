#


## WebScanner
[source](https://github.com/F3licity/WebScanner/blob/main/webscanner.py/#L10)
```python 
WebScanner(
   url, prefix = None, max_depth = None, test_external_urls = False, headers = None,
   verbose = 0
)
```


---
WebCrawler class to automatically find broken links and other issues with a website.


**Args**

* **url** (string) : The url to start crawling.
* **prefix** (string, optional) : Everything with a different prefix is treated as external.
    This allows for limiting the crawler to a subdirectory. Defaults to None.
* **max_depth** (integer, optional) : Maximum crawl depth, None is unlimited. Defaults to None.
* **test_external_urls** (bool, optional) : Test the status code of external links or not. Defaults to False.
* **headers** (dict, optional) : Custom headers dictionary for example to provide login details. Defaults to None.
* **verbose** (int, optional) : How much we output, should be 0,1 or 2. At level 0 only broken links are reported. Defaults to 0.



**Methods:**


### .crawl
[source](https://github.com/F3licity/WebScanner/blob/main/webscanner.py/#L71)
```python
.crawl(
   current_link = None, depth = 0
)
```

---
Crawl through the documentation page and return the status code of the links.

Keep track of visited links. When a new link is visited request its HTML and get all anchors found in it.
If they are external links, return their status code. If they are internal and they are relative paths,
make them first complete and then return their status.

For every link visited go deeper and deeper to visit all links found in it.


**Args**

* **current_link** (string, optional) : The current link to download and crawl (if not visited yet). Defaults to None.
* **depth** (int, optional) : The current recursive depth. Defaults to 0.


### .clean_url
[source](https://github.com/F3licity/WebScanner/blob/main/webscanner.py/#L123)
```python
.clean_url(
   url
)
```

---
Remove the query and anchors from a url.


**Args**

* **url** (string) : Url to clean.


**Returns**

* **string**  : url without anchors and query parameters.


### .is_external
[source](https://github.com/F3licity/WebScanner/blob/main/webscanner.py/#L135)
```python
.is_external(
   url
)
```

---
Check if url is in the part we want to crawl.


**Args**

* **url** (string) : The url to check.


**Returns**

* **bool**  : boolean indicating whether we treat the url as external or not.

