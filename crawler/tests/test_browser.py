import unittest
from pathlib import Path

import responses

from crawler.browser import SITEMAP_URL, Browser


def load_fixture(filename):
    return (Path(__file__).parent / "data" / filename).read_text()


class TestBrowser(unittest.TestCase):
    @responses.activate
    def test_get_sitemap_urls(self):
        sitemap_index_content = load_fixture("sitemap_index.xml")
        sitemap_url = "http://www.test.com/sitemap-index.xml"
        responses.add(responses.GET, sitemap_url, body=sitemap_index_content, status=200)

        urls = Browser._get_sitemap_urls(sitemap_url)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, sitemap_url)
        self.assertEqual(
            urls,
            ["http://www.example.com/sitemap1.xml", "http://www.example.com/sitemap2.xml"],
        )

    @responses.activate
    def test_get_sitemap_urls_with_empty_loc(self):
        sitemap_index_content = load_fixture("sitemap_index_with_empty_loc.xml")
        sitemap_url = "http://www.test.com/sitemap-index.xml"
        responses.add(responses.GET, sitemap_url, body=sitemap_index_content, status=200)

        urls = Browser._get_sitemap_urls(sitemap_url)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, sitemap_url)
        self.assertEqual(
            urls,
            ["http://www.example.com/sitemap1.xml"],
        )

    @responses.activate
    def test_extract_article_links(self):
        sitemap_content = load_fixture("sitemap_articles.xml")
        child_sitemap_url = "http://www.example.com/sitemap1.xml"
        responses.add(responses.GET, child_sitemap_url, body=sitemap_content, status=200)

        links = Browser._extract_article_links(child_sitemap_url)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, child_sitemap_url)
        self.assertEqual(
            links,
            [
                "https://www.prnewswire.com/news-releases/article-1.html",
                "https://www.prnewswire.com/news-releases/article-2.html",
            ],
        )

    @responses.activate
    def test_extract_article_links_with_empty_loc(self):
        sitemap_content = load_fixture("sitemap_articles_with_empty_loc.xml")
        child_sitemap_url = "http://www.example.com/sitemap1.xml"
        responses.add(responses.GET, child_sitemap_url, body=sitemap_content, status=200)

        links = Browser._extract_article_links(child_sitemap_url)

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].request.url, child_sitemap_url)
        self.assertEqual(
            links,
            [
                "https://www.prnewswire.com/news-releases/article-1.html",
            ],
        )

    @responses.activate
    def test_get_news_links(self):
        sitemap_index_content = load_fixture("sitemap_index.xml")
        responses.add(responses.GET, SITEMAP_URL, body=sitemap_index_content, status=200)

        sitemap_content_1 = load_fixture("sitemap1.xml")
        sitemap_content_2 = load_fixture("sitemap2.xml")
        responses.add(
            responses.GET,
            "http://www.example.com/sitemap1.xml",
            body=sitemap_content_1,
            status=200,
        )
        responses.add(
            responses.GET,
            "http://www.example.com/sitemap2.xml",
            body=sitemap_content_2,
            status=200,
        )

        links = list(Browser.get_news_links())

        self.assertEqual(len(responses.calls), 3)
        self.assertEqual(
            links,
            ["http://article1.com", "http://article2.com"],
        )

    @responses.activate
    def test_get_news_links_with_empty_sitemap_url(self):
        sitemap_index_content = load_fixture("sitemap_index_with_empty_loc.xml")
        responses.add(responses.GET, SITEMAP_URL, body=sitemap_index_content, status=200)

        sitemap_content_1 = load_fixture("sitemap1.xml")
        responses.add(
            responses.GET,
            "http://www.example.com/sitemap1.xml",
            body=sitemap_content_1,
            status=200,
        )

        links = list(Browser.get_news_links())

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(
            links,
            ["http://article1.com"],
        )
