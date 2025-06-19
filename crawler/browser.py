import logging
import xml.etree.ElementTree as ET
from collections.abc import Generator

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


SITEMAP_URL = "https://www.prnewswire.com/sitemap-news.xml"


class Browser:
    @classmethod
    def get_news_links(cls) -> Generator[str]:
        for sitemap_url in cls._get_sitemap_urls(SITEMAP_URL):
            yield from cls._extract_article_links(sitemap_url)

    @classmethod
    def _get_sitemap_urls(cls, sitemap_url: str) -> list[str]:
        """Fetch and parse a sitemap index, returning all child sitemap URLs."""
        resp = requests.get(sitemap_url)
        tree = ET.fromstring(resp.content)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        return [elem.text for elem in tree.findall("sm:sitemap/sm:loc", ns) if elem.text]

    @classmethod
    def _extract_article_links(cls, child_sitemap_url: str) -> list[str]:
        """Given a sitemap fragment, return all article URLs within it."""
        resp = requests.get(child_sitemap_url)
        tree = ET.fromstring(resp.content)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        return [elem.text for elem in tree.findall("sm:url/sm:loc", ns) if elem.text]
