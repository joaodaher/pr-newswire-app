import os
from collections.abc import Mapping
from dataclasses import asdict
from datetime import UTC, datetime

from pymongo import MongoClient
from pymongo.database import Database

from crawler.article import Article


class MongoRepository:
    def __init__(self, database_name: str, uri: str | None) -> None:
        self._client: MongoClient = MongoClient(uri)
        self._db: Database = self._client[database_name]

    def save(self, article: Article) -> Mapping:
        articles = self._db.articles
        document = asdict(article)
        document["_ingested_at"] = datetime.now(UTC)
        result = articles.insert_one(document)
        return result.inserted_id


def get_database(
    database_name: str | None = None,
    uri: str | None = None,
) -> MongoRepository:
    db_name = os.getenv("MONGO_DATABASE", "wire-scout")
    if database_name:
        db_name = database_name

    mongo_uri = uri or os.getenv("MONGO_URI")
    return MongoRepository(
        database_name=db_name,
        uri=mongo_uri,
    )
