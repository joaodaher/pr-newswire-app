import logging

import requests

from crawler.browser import Browser
from crawler.parser import NewsParser
from storage import get_database

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def scrape():
    logging.info("Starting scrape cycle")
    db = get_database()
    urls = Browser.get_news_links()

    article_ids = []
    for url in urls:
        try:
            article = NewsParser.from_url(url=url).article
            article_id = db.save_article(article)
            article_ids.append(article_id)
            logging.info(f"Saved article {article.title}")
        except (ValueError, requests.HTTPError):
            logging.exception(f"Failed to parse article at {url}")

    logging.info(f"Scrape cycle complete, stored {len(article_ids)} articles")


if __name__ == "__main__":
    scrape()
