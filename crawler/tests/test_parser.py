import unittest
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import responses

from crawler.parser import NewsParser
from models.article import Article


class TestNewsParserCornerCases(unittest.TestCase):
    """
    This test class simulates corner cases of handling the HTML content.
    """

    def setUp(self):
        self.parser = NewsParser(url="http://fake.url", html_content="<html></html>")

    @responses.activate
    def test_from_url(self):
        url = "http://fake.url"
        responses.add(responses.GET, url, body="<html></html>", status=200)
        parser = NewsParser.from_url(url)
        self.assertEqual(parser.url, url)
        self.assertEqual(parser.html_content, b"<html></html>")

    @responses.activate
    def test_from_url_http_error(self):
        url = "http://fake.url"
        responses.add(responses.GET, url, status=500)
        with self.assertRaises(Exception):
            NewsParser.from_url(url)

    def test_article_property_missing_fields(self):
        parser = NewsParser(url="http://fake.url", html_content="<html></html>")
        with self.assertRaises(ValueError):
            _ = parser.article

    def test_body_title_no_header(self):
        self.assertIsNone(self.parser._body_title)

    def test_body_title_no_h1(self):
        html_content = '<html><body><header class="release-header"></header></body></html>'
        parser = NewsParser(url="http://fake.url", html_content=html_content)
        self.assertIsNone(parser._body_title)

    def test_body_provider_no_provider(self):
        html_content = '<html><body><header class="release-header"></header></body></html>'
        parser = NewsParser(url="http://fake.url", html_content=html_content)
        self.assertIsNone(parser._body_provider)

    def test_body_date(self):
        # No header
        self.assertIsNone(self.parser._body_date)

        # Header, but no date element
        html_content = '<html><body><header class="release-header"></header></body></html>'
        parser = NewsParser(url="http://fake.url", html_content=html_content)
        self.assertIsNone(parser._body_date)

        # Date element, but empty
        html_content = '<html><body><header class="release-header"><p class="mb-no"></p></header></body></html>'
        parser = NewsParser(url="http://fake.url", html_content=html_content)
        self.assertIsNone(parser._body_date)

    def test_body_content_no_content(self):
        self.assertEqual(self.parser._body_content, "")

    def test_metadata(self):
        # No script tag
        self.assertEqual(self.parser._metadata, {})

        # Empty script tag
        html_content = '<html><body><script type="application/ld+json"></script></body></html>'
        parser = NewsParser(url="http://fake.url", html_content=html_content)
        self.assertEqual(parser._metadata, {})

        # Invalid JSON
        html_content = '<html><body><script type="application/ld+json">{,}</script></body></html>'
        parser = NewsParser(url="http://fake.url", html_content=html_content)
        self.assertEqual(parser._metadata, {})

    def test_metadata_publisher_no_publisher(self):
        html_content = '<html><body><script type="application/ld+json">{"key": "value"}</script></body></html>'
        parser = NewsParser(url="http://fake.url", html_content=html_content)
        self.assertIsNone(parser._metadata_publisher)


@dataclass
class TestSample:
    sample_file: str
    expected_title: str
    expected_provider: str
    expected_date: datetime
    expected_content_head: str
    expected_content_tail: str
    expected_metadata_headline: str
    expected_metadata_publisher: str


class ParserTestMixin:
    """
    This a test mixin that can be used to test the NewsParser class with a sample HTML file.
    Inherit from this class and define a TEST_CASE class attribute.
    """

    TEST_CASE: TestSample

    def setUp(self):
        sample_html_path = Path(__file__).parent / "data" / self.TEST_CASE.sample_file
        self.parser = NewsParser.from_file(url="https://fake.url", filepath=sample_html_path)

    def test_title(self):
        self.assertEqual(self.TEST_CASE.expected_title, self.parser.title)

    def test_date(self):
        parsed_date = self.parser.date

        self.assertIsNotNone(parsed_date)  # ensure existence
        self.assertIsInstance(parsed_date, datetime)  # ensure type
        self.assertIsNotNone(parsed_date.tzinfo)  # ensure timezone awareness

        self.assertEqual(self.TEST_CASE.expected_date, self.parser.date)  # ensure as expected

    def test_provider(self):
        self.assertEqual(self.TEST_CASE.expected_provider, self.parser.provider)

    def test_content(self):
        self.assertTrue(self.parser.content.startswith(self.TEST_CASE.expected_content_head))
        self.assertTrue(self.parser.content.strip().endswith(self.TEST_CASE.expected_content_tail))

    def test_article(self):
        article = self.parser.article
        self.assertIsNotNone(article)  # ensure existence
        self.assertIsInstance(article, Article)  # ensure type
        self.assertEqual(self.TEST_CASE.expected_title, article.title)
        self.assertEqual(self.TEST_CASE.expected_date, article.date)
        self.assertEqual(self.TEST_CASE.expected_provider, article.news_provided_by)
        self.assertTrue(article.content.startswith(self.TEST_CASE.expected_content_head))
        self.assertTrue(article.content.strip().endswith(self.TEST_CASE.expected_content_tail))

    def test_metadata_headline(self):
        self.assertEqual(self.TEST_CASE.expected_metadata_headline, self.parser._metadata_headline)

    def test_metadata_publisher(self):
        self.assertEqual(self.TEST_CASE.expected_metadata_publisher, self.parser.publisher)


class ParserTestSample001(ParserTestMixin, unittest.TestCase):
    TEST_CASE = TestSample(
        sample_file="sample_001.html",
        expected_title="Workday Names Emma Chalwin Chief Marketing Officer",
        expected_provider="Workday Inc.",
        expected_date=datetime(2023, 6, 13, 9, 5, tzinfo=timezone(timedelta(hours=-4))),
        expected_content_head="PLEASANTON, Calif., June 13, 2023",
        expected_content_tail="SOURCE Workday Inc.",
        expected_metadata_headline="Workday Names Emma Chalwin Chief Marketing Officer",
        expected_metadata_publisher="Cision PR Newswire",
    )


class ParserTestSample002(ParserTestMixin, unittest.TestCase):
    TEST_CASE = TestSample(
        sample_file="sample_002.html",
        expected_title="Drink Up, Collect 'Em All - Whataburger Releases Limited-Edition Commemorative Cups",
        expected_provider="Whataburger",
        expected_date=datetime(2025, 6, 10, 13, 39, tzinfo=timezone(timedelta(hours=-4))),
        expected_content_head="SAN ANTONIO, June 10, 2025",
        expected_content_tail="SOURCE Whataburger",
        expected_metadata_headline="Drink Up, Collect 'Em All - Whataburger Releases Limited-Edition Commemorative Cups",
        expected_metadata_publisher="Cision PR Newswire",
    )
