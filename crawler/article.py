from dataclasses import dataclass
from datetime import datetime


@dataclass
class Article:
    url: str
    title: str | None
    date: datetime | None
    news_provided_by: str | None
    content: str
