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

    def assertArticleSaved(self, article: Article):
        saved_article = self.repo._db.articles.find_one({"url": article.url})
        self.assertIsNotNone(saved_article)
        self.assertEqual(article.url, saved_article["url"])
        self.assertEqual(article.title, saved_article["title"])
        self.assertEqual(article.news_provided_by, saved_article["news_provided_by"])
        self.assertEqual(article.content, saved_article["content"])

    def assertArticlesEqual(self, articles: list[Article], expected_articles: list[Article]):
        received_articles = list(articles)
        self.assertEqual(len(received_articles), len(expected_articles))
        received_urls = {article.url for article in articles}
        expected_urls = {article.url for article in expected_articles}
        self.assertSetEqual(received_urls, expected_urls)

    def test_save_articles(self):
        articles = ArticleFactory.build_batch(size=10)
        self.assertNumberOfArticles(0)

        for article in articles:
            self.repo.save_article(article=article)
            self.assertArticleSaved(article=article)

        self.assertNumberOfArticles(expected_count=10)

    def test_get_articles(self):
        articles = ArticleFactory.create_batch(size=5)
        self.assertNumberOfArticles(5)

        with self.subTest("No filter"):
            retrieved_articles = list(self.repo.get_articles(query={}))
            self.assertArticlesEqual(retrieved_articles, articles)

        with self.subTest("With filter"):
            article_to_find = articles[0]
            retrieved_articles = list(self.repo.get_articles(query={"url": article_to_find.url}))
            self.assertArticlesEqual(retrieved_articles, [article_to_find])

        with self.subTest("With no results"):
            retrieved_articles = self.repo.get_articles(query={"url": "non-existent-url"})
            self.assertEqual(list(retrieved_articles), [])
