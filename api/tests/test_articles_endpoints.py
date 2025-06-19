import unittest
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from api.main import app
from models.article import Article
from models.tests.factories import ArticleFactory
from storage.mongo import get_database


class TestArticlesEndpoints(unittest.TestCase):
    url = "/v1/articles"

    def setUp(self):
        self.client = TestClient(app)

        self.db = get_database()
        self.db._db.articles.drop()
        self.addCleanup(self.db._db.articles.drop)

    def assertContract(self, resource: dict, article: Article):
        self.assertEqual(resource["title"], article.title)
        self.assertEqual(resource["date"], article.date.strftime("%Y-%m-%dT%H:%M:%S"))
        self.assertEqual(resource["news_provided_by"], article.news_provided_by)
        self.assertEqual(resource["content"], article.content)

    def test_get_articles_no_filters(self):
        articles = ArticleFactory.create_batch(5)

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)

        items = response.json()["items"]
        self.assertEqual(5, len(items))
        for received_item, article in zip(items, articles):
            self.assertContract(received_item, article)

    def test_get_articles_filter_by_title(self):
        article_with_title = [
            *ArticleFactory.create_batch(2, title="This is a Test Title"),
            *ArticleFactory.create_batch(2, title="This is also a Test Title"),
        ]

        ArticleFactory.create_batch(5, title="This is only noise")  # noise

        response = self.client.get(self.url + "?title=Test")  # case insensitive
        self.assertEqual(200, response.status_code)

        items = response.json()["items"]
        self.assertEqual(4, len(items))
        for received_item, article in zip(items, article_with_title):
            self.assertContract(received_item, article)

    def test_get_articles_filter_by_content(self):
        article_with_content = [
            *ArticleFactory.create_batch(2, content="This is a Test Content"),
            *ArticleFactory.create_batch(2, content="This is also a test Content"),
        ]

        ArticleFactory.create_batch(5, content="This is only noise")  # noise

        response = self.client.get(self.url + "?content=Test")  # case insensitive
        self.assertEqual(200, response.status_code)

        items = response.json()["items"]
        self.assertEqual(4, len(items))
        for received_item, article in zip(items, article_with_content):
            self.assertContract(received_item, article)

    def test_get_articles_filter_by_news_provider(self):
        article_with_provider = [
            *ArticleFactory.create_batch(2, news_provided_by="This is a Test Provider"),
            *ArticleFactory.create_batch(2, news_provided_by="This is also a Test Provider"),
        ]

        ArticleFactory.create_batch(5, news_provided_by="This is only noise")  # noise

        response = self.client.get(self.url + "?news_provider=Test")  # case insensitive
        self.assertEqual(200, response.status_code)

        items = response.json()["items"]
        self.assertEqual(4, len(items))
        for received_item, article in zip(items, article_with_provider):
            self.assertContract(received_item, article)

    def test_get_articles_filter_by_date_range(self):
        reference_date = datetime.now(tz=UTC)
        start = reference_date - timedelta(days=2)
        end = reference_date + timedelta(days=2)

        article_with_date = [
            *ArticleFactory.create_batch(2, date=start),
            *ArticleFactory.create_batch(2, date=reference_date),
            *ArticleFactory.create_batch(2, date=end),
        ]

        ArticleFactory.create_batch(5, date=start - timedelta(days=2))  # noise, before start
        ArticleFactory.create_batch(5, date=end + timedelta(days=2))  # noise, after end

        start_filter = start.strftime("%Y-%m-%dT%H:%M:%S")
        end_filter = (end + timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S")  # end is not inclusive
        response = self.client.get(self.url + f"?start_date={start_filter}&end_date={end_filter}")
        self.assertEqual(200, response.status_code)

        items = response.json()["items"]
        self.assertEqual(6, len(items))
        for received_item, article in zip(items, article_with_date):
            self.assertContract(received_item, article)

    def test_get_articles_filter_by_start_date_only(self):
        reference_date = datetime.now(tz=UTC)
        start = reference_date - timedelta(days=2)

        article_with_date = [
            *ArticleFactory.create_batch(2, date=start),
            *ArticleFactory.create_batch(2, date=reference_date),
        ]
        ArticleFactory.create_batch(2, date=reference_date - timedelta(days=7))  # noise

        start_filter = start.strftime("%Y-%m-%dT%H:%M:%S")
        response = self.client.get(self.url + f"?start_date={start_filter}")
        self.assertEqual(200, response.status_code)

        items = response.json()["items"]
        self.assertEqual(4, len(items))
        for received_item, article in zip(items, article_with_date):
            self.assertContract(received_item, article)

    def test_get_articles_filter_by_end_date_only(self):
        reference_date = datetime.now(tz=UTC)
        end = reference_date + timedelta(days=2)

        article_with_date = [
            *ArticleFactory.create_batch(2, date=reference_date),
            *ArticleFactory.create_batch(2, date=end),
        ]
        ArticleFactory.create_batch(2, date=reference_date + timedelta(days=7))  # noise

        end_filter = (end + timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S")  # end is not inclusive
        response = self.client.get(self.url + f"?end_date={end_filter}")
        self.assertEqual(200, response.status_code)

        items = response.json()["items"]
        self.assertEqual(4, len(items))
        for received_item, article in zip(items, article_with_date):
            self.assertContract(received_item, article)

    def test_get_articles_with_skip_and_limit(self):
        article_with_title = ArticleFactory.create_batch(10)

        response = self.client.get(self.url + "?skip=3&limit=4")
        self.assertEqual(200, response.status_code)

        items = response.json()["items"]
        self.assertEqual(4, len(items))

        expected_items = article_with_title[3:7]  # items 4, 5, 6, 7
        for received_item, article in zip(items, expected_items):
            self.assertContract(received_item, article)

    def test_get_articles_filter_by_date_range_invalid_date(self):
        response = self.client.get(self.url + "?start_date=invalid&end_date=invalid")
        self.assertEqual(422, response.status_code)

        error_msg = response.json()["detail"][0]["msg"]
        self.assertIn("Input should be a valid datetime", error_msg)
