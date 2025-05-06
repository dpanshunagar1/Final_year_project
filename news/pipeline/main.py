# rss_pipeline_scripts/main.py

import feedparser
import hashlib
import os
import time
import django
from categorize_articles import predict_article_category
from normalize_data import normalize_article
from deduplicate_data import is_duplicate
# from django.contrib.postgres.search import SearchVector
from datetime import datetime
from typing import Optional, List
# from pydantic import BaseModel, ValidationError


# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news.settings")  # Use the project's settings module
django.setup()

from articles.models import Article  # Import the Article model from the 'articles' app

class Author(BaseModel):
    name: str
    email: Optional[str] = None

class NormalizedArticle(BaseModel):
    title: str
    link: str
    published: Optional[datetime] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    authors: Optional[List[Author]] = None

def fetch_feed(rss_url):
    """Fetches and parses an RSS feed."""
    return feedparser.parse(rss_url)

# def normalize_article(entry):
#     """
#     Normalizes a feedparser entry into an Article Pydantic model.
#     """
#     try:
#         published_parsed = entry.get("published_parsed")
#         published_datetime = datetime.fromtimestamp(time.mktime(published_parsed)) if published_parsed else None

#         article_data = {
#             "title": entry.get("title"),
#             "link": entry.get("link"),
#             "published": published_datetime,
#             "summary": entry.get("summary"),
#             "content": entry.get("content")[0].get("value") if entry.get("content") and entry.get("content")[0].get("value") else None,
#             "authors": [Author(name=author.get("name"), email=author.get("email")) for author in entry.get("authors", []) if author.get("name")],
#         }
#         return Article(**article_data)
#     except ValidationError as e:
#         print(f"Normalization Error: {e}")
#         print(f"Problematic entry keys: {entry.keys()}")
#         return None

# def generate_sha256(content: str) -> str:
#     """Generates a SHA-256 hash of the content."""
#     if content is None:
#         return ""
#     encoded_content = content.encode('utf-8')
#     return hashlib.sha256(encoded_content).hexdigest()

def process_feed(rss_url):
    feed = fetch_feed(rss_url)
    for entry in feed.entries:
        normalized_article = normalize_article(entry)
        if normalized_article:
            article_hash = hashlib.sha256(normalized_article.link.encode()).hexdigest()
            if not is_duplicate(article_hash,existing_hashes=set(Article.objects.values_list('sha256_hash', flat=True))):
                # Categorize the article *after* normalization and deduplication
                predicted_category = predict_article_category(
                    normalized_article.title,
                    normalized_article.summary,
                    normalized_article.content
                )
                
                # Correct way of handling authors
                
                # authors_list = [author.name for author in normalized_article.authors] if normalized_article.authors else []
                article = Article(
                    title=normalized_article.title,
                    link=normalized_article.link,
                    published=normalized_article.published,
                    summary=normalized_article.summary,
                    content=normalized_article.content,
                    authors=authors_list,
                    sha256_hash=article_hash,
                    # search_vector=SearchVector('title', 'summary', 'content', config='english', weight='A') +
                    #               SearchVector('authors__name', config='english', weight='B'),
                    category=predicted_category  # Store the predicted category
                )
                try:
                    article.save()
                    print(f"Article '{article.title}' processed, categorized as '{predicted_category}', and stored.")
                except Exception as e:
                    print(f"Error saving article '{normalized_article.title}': {e}")
            else:
                print(f"Duplicate article found: {normalized_article.title}")

if __name__ == '__main__':
    rss_feeds = [
    "http://feeds.bbci.co.uk/news/rss.xml",
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://feeds.reuters.com/reuters/topNews",
    "http://rss.nytimes.com/nyt/rss/HomePage",
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "http://rss.cnn.com/rss/cnn_world.rss",
    "http://feeds.reuters.com/reuters/worldNews",
    "http://feeds.nytimes.com/nyt/rss/Technology",
    "https://www.thehindu.com/news/national/india/rss.xml",
    "https://indianexpress.com/section/latest-news/feed/",
    "http://www.latimes.com/local/california/rss2.0.xml",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.nytimes.com/nyt/rss/Business",
    "https://www.business-standard.com/rss/latest-news-1.rss",
    "http://feeds.feedburner.com/TechCrunch/",
    "https://www.theverge.com/rss/index.xml",
    "http://feeds.wired.com/wired/index",
    "http://www.espn.com/espn/rss/news",
    "http://feeds.bbci.co.uk/sport/rss.xml",
]
    for url in rss_feeds:
        process_feed(url)

    print("Pipeline finished processing all feeds.")