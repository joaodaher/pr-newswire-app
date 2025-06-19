import unittest

from models.article import Article
from models.tests.factories import ArticleFactory
from storage.mongo import get_database


class TestMongoRepository(unittest.TestCase):
    def setUp(self):
        self.repo = get_database()
        self.addCleanup(self.repo._db.articles.drop)

    def assertNumberOfArticles(self, expected_count: int):
        actual_count = self.repo._db.articles.count_documents({})
        self.assertEqual(expected_count, actual_count)

    def assert_article_saved(self, article: Article):
        saved_article = self.repo._db.articles.find_one({"url": article.url})
        self.assertIsNotNone(saved_article)
        self.assertEqual(article.url, saved_article["url"])
        self.assertEqual(article.title, saved_article["title"])
        self.assertEqual(article.news_provided_by, saved_article["news_provided_by"])
        self.assertEqual(article.content, saved_article["content"])

    def test_save_articles(self):
        articles = ArticleFactory.build_batch(size=10)
        self.assertNumberOfArticles(0)

        for article in articles:
            self.repo.save_article(article=article)
            self.assert_article_saved(article=article)

        self.assertNumberOfArticles(expected_count=10)
