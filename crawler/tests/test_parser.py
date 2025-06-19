import unittest
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from crawler.article import Article
from crawler.parser import NewsParser


@dataclass
class TestSample:
    sample_file: str
    expected_title: str
    expected_provider: str
    expected_date: datetime
    expected_content_head: str
    expected_content_tail: str


class ParserTestMixin:
    """
    This a test mixin that can be used to test the NewsParser class.
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


class ParserTestSample001(ParserTestMixin, unittest.TestCase):
    TEST_CASE = TestSample(
        sample_file="sample_001.html",
        expected_title="Workday Names Emma Chalwin Chief Marketing Officer",
        expected_provider="Workday Inc.",
        expected_date=datetime(2023, 6, 13, 9, 5, tzinfo=timezone(timedelta(hours=-4))),
        expected_content_head="PLEASANTON, Calif., June 13, 2023",
        expected_content_tail="SOURCE Workday Inc.",
    )


class ParserTestSample002(ParserTestMixin, unittest.TestCase):
    TEST_CASE = TestSample(
        sample_file="sample_002.html",
        expected_title="Drink Up, Collect 'Em All - Whataburger Releases Limited-Edition Commemorative Cups",
        expected_provider="Whataburger",
        expected_date=datetime(2025, 6, 10, 13, 39, tzinfo=timezone(timedelta(hours=-4))),
        expected_content_head="SAN ANTONIO, June 10, 2025",
        expected_content_tail="SOURCE Whataburger",
    )
