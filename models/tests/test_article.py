import unittest

from models.article import Article
from models.tests.factories import ArticleFactory
from storage.mongo import get_database


class TestArticle(unittest.TestCase):
    def setUp(self):
        self.db = get_database()
        self.addCleanup(self.db._db.articles.drop)

    def assertArticleSaved(self, article: Article):
        saved_article = self.db._db.articles.find_one({"url": article.url})
        self.assertIsNotNone(saved_article)

    def assertArticleNotSaved(self, article: Article):
        saved_article = self.db._db.articles.find_one({"url": article.url})
        self.assertIsNone(saved_article)

    def test_build(self):
        article = ArticleFactory.build()
        self.assertArticleNotSaved(article)

    def test_create(self):
        article = ArticleFactory.create()
        self.assertArticleSaved(article)

    def test_build_many(self):
        articles = ArticleFactory.build_batch(size=10)
        for article in articles:
            self.assertArticleNotSaved(article)

    def test_create_many(self):
        articles = ArticleFactory.create_batch(size=10)
        for article in articles:
            self.assertArticleSaved(article)
