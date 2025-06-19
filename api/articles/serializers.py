from collections.abc import Iterable
from typing import Self

from pydantic import BaseModel

from models.article import Article


class ArticleListResource(BaseModel):
    title: str
    date: str
    news_provided_by: str
    content: str

    @classmethod
    def from_article(cls, article: Article) -> Self:
        return cls(
            title=article.title,
            date=article.date.strftime("%Y-%m-%dT%H:%M:%S"),
            news_provided_by=article.news_provided_by,
            content=article.content,
        )


class ArticleListResponse(BaseModel):
    items: list[ArticleListResource]

    @classmethod
    def from_articles(cls, articles: Iterable[Article]) -> Self:
        return cls(
            items=[ArticleListResource.from_article(article) for article in articles],
        )
