import logging

import requests

from crawler.browser import Browser
from crawler.parser import NewsParser

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def scrape():
    logging.info("Starting scrape cycle")
    urls = Browser.get_news_links()

    articles = []
    for url in urls:
        try:
            article = NewsParser.from_url(url=url).article
            articles.append(article)
        except (ValueError, requests.HTTPError):
            logging.exception(f"Failed to parse article at {url}")

    logging.info(f"Scrape cycle complete, stored {len(articles)} articles")


if __name__ == "__main__":
    scrape()
