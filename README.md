# WebScanner

A simple webcrawler to detect broken links in websites recursively using Python.

## How to use
--------------
You can use and extend the tool to easily crawl a website and check for broken links and other errors.  
Download the pageCrawler.py and call it from the terminal using:

    python3 pageCrawler.py URL_TO_CRAWL

Check out all the options using

    python3 pageCrawler.py --help

### Run using Docker
Use the one-liner below to immediately use the WebScanner from DockerHub:

```zsh
docker run --rm emeraldit/webscanner:1.0.1 URL_TO_CRAWL
```

To run the docker command and send the output to your Slack, execute the image like this:

```zsh
docker run --rm -e SLACK_BOT_TOKEN='your-slack-token' emeraldit/webscanner:1.0.1 --channel_id SLACK_ID URL_TO_CRAWL
```

You can also easily run the script using Docker.  
Build the image: 

```zsh
docker build --tag emeraldit/webscanner:1.0.1 .
```

Run the image

```zsh
docker run --rm \
  --name webscanner.container \
  emeraldit/webscanner:1.0.1 \
  --help
```

or on powershell:

```powershell
docker run --rm `
  --name webscanner.container `
  emeraldit/webscanner:1.0.1 `
  --help
```

### Use in your own project
You can also use the class directly in your own python code:
``` py linenums="1"
from webscanner import WebScanner

crawler = WebScanner(
    URL_TO_CRAWL,
    prefix=OPTIONAL_PREFIX,
    max_depth=2,
    test_external_urls=True,
    verbose=2,
)
crawler.crawl()
```

The *prefix* determines which links are crawled, for example you can limit the crawling to a specific subdirectory of a
domain such as https://domain.com/dir/
Everything above the /dir/ will be ignored, when setting the prefix to this url.

The *max_depth* determines how deep the crawler goes, for example if set to 1, only the links of the initial page are
followed and the process stops. If set to 2, all links of the initial page and all following links from the pages that
follow the initial page are crawled.

### slackHandler

The WebScanner can send the results of the run directly to your Slack channel.

By providing the `--channel_id` or `-cid` flag, in execution, you can provide the ID of the Slack
channel in which you would like to post the results.

In order to allow the WebScanner to send messages to your Slack, you need to expose, into your environment
variables, the `SLACK_BOT_TOKEN`. Curious where to find this token? Read further on
[Slack's documentation](https://slack.com/help/articles/215770388-Create-and-regenerate-API-tokens).


## Further development
--------------
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
Make sure to check out the CONTRIBUTING.md about the house rules.
Start developing!

### Documentation
To contribute please also update the documentation.
You can download the required packages from docs-requirements.txt (`pip install -r docs-requirements.txt`).

Install the documentation requirements:

    pip install -r docs-requirements.txt

Build the documentation:

```zsh
gendocs --config mkgendocs.yml
```

You can then do `mkdocs serve` and access it on http://127.0.0.1:8000/


![](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
![](https://img.shields.io/badge/contributions-welcome-orange.svg)
![](https://img.shields.io/badge/license-MIT-blue.svg)