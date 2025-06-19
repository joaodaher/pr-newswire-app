import factory

from models.article import Article
from storage.mongo import get_database


class ArticleFactory(factory.Factory):
    class Meta:
        model = Article

    url = factory.Faker("url")
    title = factory.Faker("sentence")
    date = factory.Faker("date_time")
    news_provided_by = factory.Faker("company")
    content = factory.Faker("text")

    @classmethod
    def create(cls, **kwargs) -> Article:
        article = super().create(**kwargs)
        db = get_database()
        db.save_article(article)
        return article
