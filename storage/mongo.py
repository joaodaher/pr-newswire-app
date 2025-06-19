import os
from collections.abc import Generator, Mapping
from datetime import UTC, datetime
from typing import Any

from pymongo import MongoClient
from pymongo.cursor import Cursor
from pymongo.database import Database

from models.article import Article


class MongoRepository:
    def __init__(self, database_name: str, uri: str | None) -> None:
        self._client: MongoClient = MongoClient(uri)
        self._db: Database = self._client[database_name]

    def save_article(self, article: Article) -> Mapping:
        articles_collection = self._db.articles
        document = article.model_dump() | {"_ingested_at": datetime.now(UTC)}
        result = articles_collection.insert_one(document)
        return result.inserted_id

    def get_articles(self, query: dict[str, Any]) -> Generator[Article]:
        articles_collection = self._db.articles
        articles_cursor: Cursor = articles_collection.find(query)
        for article in articles_cursor:
            yield Article(
                title=article.get("title", ""),
                content=article.get("content", ""),
                url=article.get("url", ""),
                date=article.get("date"),
                news_provided_by=article.get("news_provided_by", ""),
            )


def get_database(
    database_name: str | None = None,
    uri: str | None = None,
) -> MongoRepository:
    db_name = database_name or os.getenv("MONGO_DATABASE", "wire-scout")

    mongo_uri = uri or os.getenv("MONGO_URI")
    return MongoRepository(
        database_name=db_name,
        uri=mongo_uri,
    )
