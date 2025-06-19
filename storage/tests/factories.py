import factory

from crawler.article import Article


class ArticleFactory(factory.Factory):
    class Meta:
        model = Article

    url = factory.Faker("url")
    title = factory.Faker("sentence")
    date = factory.Faker("date_time")
    news_provided_by = factory.Faker("company")
    content = factory.Faker("text")
