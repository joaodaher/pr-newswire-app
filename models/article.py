from datetime import datetime

from pydantic import BaseModel


class Article(BaseModel):
    url: str
    title: str
    date: datetime
    news_provided_by: str
    content: str
