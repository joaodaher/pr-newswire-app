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

## Features

- **Web Crawler**: a crawler that fetches news articles from PR Newswire's sitemaps.
- **Data Extraction**: parses HTML to extract key information from articles, including title, publication date, provider, and full content.
- **RESTful API**: a FastAPI application that provides endpoints to search and filter the stored news articles.
- **MongoDB Integration**: uses MongoDB to store and retrieve article data efficiently.
- **Containerized**: fully containerized with Docker and Docker Compose for easy and consistent deployment.
- **Parallel Operations**: the crawler uses a thread pool to fetch and process articles concurrently, improving performance.

## Tech Stack

- **Backend**: Python 3.13, FastAPI
- **Database**: MongoDB
- **Web Scraping**: BeautifulSoup4, Requests, lxml
- **Containerization**: Docker, Docker Compose
- **Dependency Management**: uv
- **Testing**: Pytest, httpx, factory-boy
- **Linting & Formatting**: Ruff

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

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
