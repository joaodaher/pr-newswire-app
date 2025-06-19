[![Github CI](https://github.com/joaodaher/pr-newswire-app/workflows/Github%20CI/badge.svg)](https://github.com/joaodaher/pr-newswire-app/actions)
[![Maintainability](https://qlty.sh/badges/7614d4be-0c5f-475d-9508-03b8dd4d1072/maintainability.svg)](https://qlty.sh/gh/joaodaher/projects/pr-newswire-app)
[![Code Coverage](https://qlty.sh/badges/7614d4be-0c5f-475d-9508-03b8dd4d1072/test_coverage.svg)](https://qlty.sh/gh/joaodaher/projects/pr-newswire-app)

[![python](https://img.shields.io/badge/python-3.13-blue.svg)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-green.svg)]()
[![MongoDB](https://img.shields.io/badge/MongoDB-green.svg)]()
[![Docker](https://img.shields.io/badge/Docker-blue.svg)]()

# Wire Scout

## Overview

Wire Scout is a Python-based web scraping application designed to extract and store news articles from PR Newswire. It consists of a web crawler that fetches article data and a FastAPI-powered API to query the stored articles. The entire application is containerized with Docker for easy setup and deployment.

## Tech Stack

- **Backend**: Python 3.13, FastAPI
- **Database**: MongoDB
- **Web Scraping**: BeautifulSoup4, Requests, lxml
- **Containerization**: Docker, Docker Compose
- **Dependency Management**: uv
- **Testing**: Pytest, httpx, factory-boy
- **Linting & Formatting**: ruff

## Architecture

The application is composed of three main services:

1.  **Crawler**: a Python script that can periodically scrapes PR Newswire for new articles. It parses the HTML and stores the structured data into the MongoDB database.
2.  **API**: a FastAPI server that exposes endpoints to interact with the data stored in the database.
3.  **Storage**: A MongoDB instance that serves as the data store for the articles.

![image](https://github.com/user-attachments/assets/0c8bd07f-bc69-4ad4-ad7f-63108135609b)


## Getting Started

You can run the application using Docker (recommended) or set it up locally for development.

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.13+ (for local setup)
- [uv](https://github.com/astral-sh/uv) (for local setup)

### Running with Docker (Recommended)

This is the easiest way to get the application up and running.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/joaodaher/pr-newswire-app.git
    cd pr-newswire-app
    ```

2.  **Build and start the services:**
    Use the `Makefile` to build and run the services in detached mode:
    ```bash
    make run-all
    ```
    This command will start the API server, the MongoDB database, and run the crawler once.

3.  **Access the API:**
    The API will be available at [http://localhost:8000](http://localhost:8000). You can access the interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

4.  **Cleaning up:**
    To remove the containers and volumes, run:
    ```bash
    make clean-up
    ```

### Local Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/joaodaher/pr-newswire-app.git
    cd pr-newswire-app
    ```

2.  **Install dependencies:**
    Use the `Makefile` to install all required dependencies.
    ```bash
    make dependencies
    ```

3.  **Run the application:**
    You'll need a running MongoDB instance. You can start one using Docker:
    ```bash
    docker-compose up -d mongo
    ```

    Then, you can run the API and the crawler in separate terminal windows:

    **Run the API server:**
    ```bash
    make run-api
    ```
    The API will be available at [http://localhost:8000](http://localhost:8000).

    **Run the crawler:**
    ```bash
    make run-crawler
    ```

## Usage

### Crawler

The crawler is designed to be run as a script. When executed, it fetches all article URLs from the PR Newswire sitemap, scrapes the content of each article, and stores it in the MongoDB database.

You can run the crawler manually using Docker:
```bash
docker-compose run --rm crawler
```
Or locally (if you followed the local setup):
```bash
make run-crawler
```

### API Endpoints

The API provides one main endpoint to query the articles.

#### `GET /v1/articles`

Retrieves a list of articles. It supports filtering by the following query parameters:

- `title` (str): Filter by text in the article title (case-insensitive regex).
- `content` (str): Filter by text in the article content (case-insensitive regex).
- `start_date` (datetime): Filter for articles published on or after this date (ISO 8601 format).
- `end_date` (datetime): Filter for articles published on or before this date (ISO 8601 format).
- `news_provider` (str): Filter by the news provider's name (case-insensitive regex).

**Example using `curl`:**
```bash
curl -X GET "http://localhost:8000/v1/articles?title=technology&start_date=2023-01-01T00:00:00"
```

## Testing

The project uses `pytest` for testing. To run the test suite, use the `Makefile` command:

```bash
make test
```

This command will run linting checks with `ruff` and then execute the unit tests with `pytest`, providing a coverage report at the end.


## Set for Success

Wire Scout is architected with extensibility and maintainability at its core. The modular design and comprehensive testing infrastructure position it as a robust foundation that can easily scale to support multiple news sources and expand functionality.

### Modular Architecture for Scalability

The application follows a clean, modular architecture that separates concerns across distinct components:

- **`models/`**: Domain models with clear data structures that can be extended for new content types
- **`storage/`**: Abstracted data persistence layer with MongoDB implementation that can be swapped or extended
- **`crawler/`**: Pluggable crawling system designed to accommodate different news sources
- **`api/`**: RESTful API layer built with FastAPI for high-performance, scalable endpoints

This separation allows for:
- **Multi-source support**: adding new news sources like Reuters, AP News, or Bloomberg requires only implementing the parser interface
- **Storage flexibility**: the repository pattern enables easy switching between databases (MongoDB, PostgreSQL, ElasticSearch)
- **API evolution**: new endpoints and features can be added without affecting the core crawling logic

### Comprehensive Testing Suite

Wire Scout implements a sophisticated testing framework that ensures reliability and facilitates confident development:

#### Factory-Based Test Data Generation
The project uses **Factory Boy** to create realistic, consistent test data:

```python
class ArticleFactory(factory.Factory):
    class Meta:
        model = Article

    url = factory.Faker("url")
    title = factory.Faker("sentence")
    date = factory.Faker("date_time")
    news_provided_by = factory.Faker("company")
    content = factory.Faker("text")
```

This approach provides:
- **Deterministic testing**: Consistent, reproducible test scenarios
- **Data isolation**: Each test gets fresh, clean data
- **Realistic scenarios**: Faker-generated data mimics real-world content

#### Multi-Layer Test Coverage

The testing strategy covers every architectural layer:

**1. Unit Tests**
- Model validation and business logic (`models/tests/`)
- Data storage operations (`storage/tests/`)
- HTML parsing and extraction (`crawler/tests/`)
- API endpoint behavior (`api/tests/`)

**2. Integration Tests**
- End-to-end API workflows with real database operations
- Parser testing with authentic HTML samples from target websites
- Cross-component data flow validation

**3. Contract Testing**
- Consistent API response validation across all endpoints
- Database schema compliance verification
- Parser output validation against expected article structures

#### Test Infrastructure Highlights

**Real-World Data Testing**: The crawler tests use actual HTML samples from PR Newswire (`crawler/tests/data/`), ensuring the parser works with real-world content variations.

**Mixin-Based Test Organization**: The `ParserTestMixin` pattern allows easy addition of new test cases for different news sources:

```python
class ParserTestSample001(ParserTestMixin, unittest.TestCase):
    TEST_CASE = TestSample(
        sample_file="sample_001.html",
        expected_title="Workday Names Emma Chalwin Chief Marketing Officer",
        expected_provider="Workday Inc.",
        # ... additional test parameters
    )
```

- **Automated Quality Assurance**: The testing pipeline includes:
- **Ruff** for code formatting and linting
- **Typing**: extensivelly typed
- **pytest** with coverage reporting
- **Random test execution order** to catch test dependencies
- **Comprehensive assertions** with custom helper methods

### Development Workflow Excellence

The project implements best practices for development efficiency:

- **Simple Commands**: `make test`, `make run-api`, `make run-crawler` for streamlined development
- **Dependency Management**: uv-based dependency resolution with lock files for reproducible environments
- **Docker Integration**: one-command setup with `make run-all` for consistent deployment
- **Code Quality**: automated formatting and linting with configurable rules

This foundation makes Wire Scout not just a PR Newswire crawler, but a **platform for news aggregation** that can grow to support any number of sources while maintaining high code quality and reliability.



## Next Steps

Here are some potential improvements and future directions for the project:

### Scalability

The current crawler uses a `ThreadPoolExecutor` for concurrency, which is effective but can be improved. Given that the crawler's tasks (making HTTP requests and database calls) are I/O-bound, a transition to a fully asynchronous architecture would offer better performance and scalability.

-   **Async Implementation**: refactor the crawler using `asyncio`. This would involve replacing `requests` with `aiohttp` for non-blocking HTTP requests and using `motor` as the asynchronous driver for MongoDB. This would allow the application to handle many concurrent operations with minimal resource overhead.

-   **Worker-Based System**: for even greater scalability, especially in a distributed environment, a task queue system like `Celery` with `RabbitMQ` or `Redis` as a message broker could be implemented. This would decouple the task scheduling from the execution and allow for multiple worker nodes to process articles in parallel.

### Resiliency

To ensure the crawler can run reliably for long periods, it needs to be more resilient to network issues and server-side limitations.

-   **Rate Limiting**: implement a strategy to handle HTTP 429 (Too Many Requests) errors. This can be achieved by adding retry logic with exponential backoff and jitter to the HTTP client, ensuring the crawler automatically slows down when it's making too many requests. Tenacity is a good library to handle this.
-   **Error Handling**: improve error handling for failed requests or parsing errors, so that a single failed article does not stop the entire scraping process.

### Continuity and Data Integrity

To maintain a clean and efficient dataset, it's important to prevent data duplication.

-   **Duplicate Prevention**: before attempting to scrape and save an article, the crawler should first check if the article's URL already exists in the database. A more robust approach would be to enforce uniqueness at the database level by creating a unique index on the `url` field in the `articles` collection. This would prevent any race conditions that might lead to duplicate entries.

### Performance Optimization

As the number of articles grows, database performance will become a bottleneck.

-   **Database Indexing**: to optimize query performance, indexes should be added to the MongoDB `articles` collection. Based on the current API, creating indexes on `date`, `news_provided_by`, and the fields used for text search (`title`, `content`) would dramatically reduce query times by avoiding collection-wide scans.

### API Enhancements

The API can be extended with features common to production-grade services.

-   **Authentication**: secure the API endpoints to control access. FastAPI has built-in support for security schemes like **API Keys**, which could be implemented to ensure that only authorized clients can access the data.
-   **Caching**: introduce a caching layer to reduce latency and decrease the load on the database. A solution like `Redis` could be used to cache the results of common API queries. For example, requests for recently published articles could be cached for a short period.
-   **API Gateway**: implement an API gateway to handle the routing and authentication of requests. This would allow for a more secure and scalable API.


### Monitoring and Logging

-   **Monitoring**: implement a monitoring system to track the health and performance of the application. This could include metrics like request rates, response times, and error rates.
-   **Logging**: implement a logging system to track the activity of the application. This could include logging requests and responses, as well as any errors that occur.

Sentry and Datadog are good options.

### Documentation

-   **API Documentation**: improve the API documentation to make it more comprehensive and easy to understand. OpenAPI 3.0 format is the standard for API documentation and clients can generate clients in multiple languages.


### Full Site Crawling

The current crawler only crawls the sitemap of PR Newswire. It could be extended to crawl the entire site, if allowed by the terms of service.

This would be a more comprehensive approach and would allow the crawler to find more articles.

This can be achieved by detecting links to other pages and following them. The Parser already handles the scrapping, so it would just need to be extract links and enqueue them for processing.

The Browser Task might need some tweaks:
- crawl the homepage as well, where we hope that new articles are always published.
- increase its execution frequency, to assure that we don't miss any new articles.


For a more robust approach, a **Graph** could be used to store the links and their relationships. This would allow for a more efficient way to find all the articles in the site.

This might also offer more data to the API, like the ability to find articles that are related to a given article. Neo4J is a good option for a graph database and could even replace MongoDB entirely.



## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
