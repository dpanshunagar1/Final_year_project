# If in normalize_data.py
from pydantic import BaseModel, ValidationError
from datetime import datetime
from typing import Optional, List
import time

class Author(BaseModel):
    name: str
    email: Optional[str] = None

class Article(BaseModel):
    title: str
    link: str
    published: Optional[datetime] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    authors: Optional[List[Author]] = None

def normalize_article(entry):
    """
    Normalizes a feedparser entry into an Article Pydantic model.
    """
    try:
        published_parsed = entry.get("published_parsed")
        published_datetime = datetime.fromtimestamp(time.mktime(published_parsed)) if published_parsed else None

        article_data = {
            "title": entry.get("title"),
            "link": entry.get("link"),
            "published": published_datetime,
            "summary": entry.get("summary"),
            "content": entry.get("content")[0].get("value") if entry.get("content") and entry.get("content")[0].get("value") else None,
            "authors": [Author(name=author.get("name"), email=author.get("email")) for author in entry.get("authors", []) if author.get("name")],
        }
        return Article(**article_data)
    except ValidationError as e:
        print(f"Normalization Error: {e}")
        print(f"Problematic entry keys: {entry.keys()}")
        return None



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

# If normalize_article is directly in main.py, update it there similarly