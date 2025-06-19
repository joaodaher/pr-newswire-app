from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from api.articles.serializers import ArticleListResponse
from storage.mongo import MongoRepository, get_database

router = APIRouter()


def get_db() -> MongoRepository:
    return get_database()


@router.get("/v1/articles", response_model=ArticleListResponse)
def get_articles(
    db: Annotated[MongoRepository, Depends(get_db)],
    title: str | None = Query(None, description="Text in title"),
    content: str | None = Query(None, description="Text in content"),
    start_date: datetime | None = Query(None, description="Start date for filtering"),
    end_date: datetime | None = Query(None, description="End date for filtering"),
    news_provider: str | None = Query(None, description="News provider"),
):
    query: dict[str, Any] = {}
    if title:
        query["title"] = {"$regex": title, "$options": "i"}
    if content:
        query["content"] = {"$regex": content, "$options": "i"}
    if news_provider:
        query["news_provided_by"] = {"$regex": news_provider, "$options": "i"}

    if start_date or end_date:
        date_filter = {}
        if start_date:
            date_filter["$gte"] = start_date
        if end_date:
            date_filter["$lte"] = end_date
        if date_filter:
            query["date"] = date_filter

    articles = db.get_articles(query)
    return ArticleListResponse.from_articles(articles=articles)
