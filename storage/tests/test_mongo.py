import unittest

from crawler.article import Article
from storage.mongo import get_database
from storage.tests.factories import ArticleFactory


class TestMongoRepository(unittest.TestCase):
    def setUp(self):
        self.repo = get_database()
        self.addCleanup(self.repo._db.articles.drop)

    def assert_article_saved(self, article: Article):
        saved_article = self.repo._db.articles.find_one({"url": article.url})
        self.assertIsNotNone(saved_article)
        self.assertEqual(article.url, saved_article["url"])
        self.assertEqual(article.title, saved_article["title"])
        self.assertEqual(article.news_provided_by, saved_article["news_provided_by"])
        self.assertEqual(article.content, saved_article["content"])

    def test_save_articles(self):
        articles = ArticleFactory.create_batch(size=10)
        for article in articles:
            self.repo.save(article=article)
            self.assert_article_saved(article=article)
