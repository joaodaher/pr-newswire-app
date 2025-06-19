import logging
from concurrent.futures import ThreadPoolExecutor

import requests

from crawler.browser import Browser
from crawler.parser import NewsParser
from storage import get_database

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


db = get_database()


def _parse_and_store(url: str) -> str | None:
    """
    Parse an article from a URL and store it in the database.
    """
    try:
        article = NewsParser.from_url(url=url).article
        article_id = db.save_article(article)
        logging.info(f"Saved article {article.title}")
        return str(article_id)
    except (ValueError, requests.HTTPError):
        logging.exception(f"Failed to parse article at {url}")
        return None


def scrape():
    logging.info("Starting scrape cycle")
    urls = Browser.get_news_links()

    pool = ThreadPoolExecutor()

    article_ids = []
    for article_id in pool.map(_parse_and_store, urls):
        if article_id is not None:
            article_ids.append(article_id)

    logging.info(f"Scrape cycle complete, stored {len(article_ids)} articles")


if __name__ == "__main__":
    scrape()
