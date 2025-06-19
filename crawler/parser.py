import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import cached_property
from pathlib import Path
from typing import Self

import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement
from dateutil import parser

from models.article import Article

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


SITEMAP_URL = "https://www.prnewswire.com/sitemap-news.xml"
TZINFOS = {"ET": timezone(timedelta(hours=-4))}  # TODO: extend to more timezones


@dataclass
class NewsParser:
    url: str
    html_content: str | None = None

    @classmethod
    def from_url(cls, url: str) -> Self:
        html_content = cls._get_html(url=url)
        return cls(url=url, html_content=html_content)

    @classmethod
    def from_file(cls, url: str, filepath: Path) -> Self:
        with filepath.open() as f:
            html_content = f.read()
        return cls(url=url, html_content=html_content)

    @cached_property
    def _soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.html_content, "lxml")

    @cached_property
    def article(self) -> Article:
        title = self.title
        date = self.date
        provider = self.provider

        if not all([title, date, provider]):
            raise ValueError(f"Missing required fields: title={title}, date={date}, provider={provider}")

        return Article(url=self.url, title=title, date=date, news_provided_by=provider, content=self.content)

    @property
    def title(self) -> str | None:
        return self._body_title or self._metadata_headline

    @property
    def date(self) -> datetime | None:
        """Extract date from metadata or body header."""
        return self._body_date or self._metadata_date_published or self._metadata_date_modified

    @property
    def provider(self) -> str | None:
        """Extract provider from body header"""
        return self._body_provider

    @property
    def publisher(self) -> str | None:
        return self._metadata_publisher

    @property
    def content(self) -> str:
        """Extract main content of the article."""
        return self._body_content.strip() if self._body_content else ""

    @classmethod
    def _get_html(cls, url: str) -> str:
        """Helper to fetch raw HTML content from a URL."""
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.content

    # --------------------
    # BODY EXTRACTION
    # --------------------

    @cached_property
    def _body_header(self) -> PageElement | None:
        return self._soup.find("header", class_="release-header")

    @property
    def _body_title(self) -> str | None:
        if not self._body_header:
            return None
        title_el = self._body_header.find("h1")
        return title_el.get_text(strip=True) if title_el else None

    @property
    def _body_provider(self) -> str | None:
        if not self._body_header:
            return None
        provider_el = self._body_header.select_one("a > strong")
        if provider_el:
            return provider_el.get_text(strip=True)
        return None

    @property
    def _body_date(self) -> datetime | None:
        if not self._body_header:
            return None
        date_el = self._body_header.find("p", class_="mb-no")
        if not date_el:
            return None

        date_str = date_el.get_text(strip=True)
        if not date_str:
            return None

        return parser.parse(date_str, tzinfos=TZINFOS)

    @property
    def _body_content(self) -> str:
        """
        Extract the main content of the article:
        After the header, and right before the Ad section.
        """
        content_el = self._soup.select_one("section.release-body .col-lg-10")
        return content_el.get_text() if content_el else ""

    # --------------------
    # METADATA EXTRACTION
    # --------------------

    @cached_property
    def _metadata(self) -> dict:
        script_tag = self._soup.find("script", type="application/ld+json")
        if not (script_tag and hasattr(script_tag, "string") and script_tag.string):
            return {}
        try:
            return json.loads(script_tag.string)
        except (json.JSONDecodeError, KeyError):
            logging.warning("Could not parse date from JSON script.")
            return {}

    @property
    def _metadata_date_published(self) -> datetime | None:
        date_str = self._metadata.get("datePublished")
        if date_str:
            return datetime.fromisoformat(date_str)
        return None

    @property
    def _metadata_date_modified(self) -> datetime | None:
        date_str = self._metadata.get("dateModified")
        if date_str:
            return datetime.fromisoformat(date_str)
        return None

    @property
    def _metadata_headline(self) -> str | None:
        return self._metadata.get("headline")

    @property
    def _metadata_publisher(self) -> str | None:
        return self._metadata.get("publisher", {}).get("name")
