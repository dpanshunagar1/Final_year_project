# articles/management/commands/process_feeds.py
from django.core.management.base import BaseCommand
from articles.models import RSSFeed, Article
import requests
import feedparser
import hashlib
from datetime import datetime, timezone

class Command(BaseCommand):
    help = 'Fetches and processes articles from RSS feeds'

    def normalize_article(self, entry, feed_source, default_category):
        """Normalizes a single feed entry."""
        normalized = {}
        normalized['title'] = entry.get('title')
        normalized['author'] = entry.get('author') or entry.get('dc_creator')
        normalized['url'] = entry.get('link')
        normalized['content'] = entry.get('content', [{}])[0].get('value') if entry.get('content') and entry.get('content') else entry.get('summary')
        normalized['description'] = entry.get('summary')
        normalized['source_name'] = feed_source
        normalized['category'] = default_category

        if 'published_parsed' in entry and entry.published_parsed:
            normalized['published_date'] = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        elif 'updated_parsed' in entry and entry.updated_parsed:
            normalized['published_date'] = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
        else:
            normalized['published_date'] = None

        image_url = None
        if 'media_content' in entry and entry.media_content and len(entry.media_content) > 0:
            image_url = entry.media_content[0].get('url')
        elif 'image' in entry and entry.get('image').get('href'):
            image_url = entry.get('image').get('href')
        elif 'enclosures' in entry and entry.get('enclosures') and len(entry.get('enclosures')) > 0 and 'url' in entry.get('enclosures')[0]:
            image_url = entry.get('enclosures')[0].get('url')
        normalized['image_url'] = image_url

        content_to_hash = normalized.get('title', '') + normalized.get('url', '') + normalized.get('content', '')
        normalized['sha256_hash'] = hashlib.sha256(content_to_hash.encode('utf-8')).hexdigest()

        return normalized

    def check_duplicate(self, article_hash):
        """Checks if an article with the given SHA256 hash already exists."""
        return Article.objects.filter(sha256_hash=article_hash).exists()

    def predict_article_category(self, title, description, content):
        """Placeholder for your article category prediction logic."""
        return "General"

    def process_feed(self, rss_feed):
        """Fetches and processes articles from a single RSS feed object."""
        rss_url = rss_feed.url
        feed_source_from_model = rss_feed.source_name
        default_category = rss_feed.category

        try:
            response = requests.get(rss_url, timeout=10)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            feed_source_from_feed = feed.get('feed', {}).get('title')
            feed_source = feed_source_from_model or feed_source_from_feed or "Unknown Source"

            for entry in feed.entries:
                normalized_article = self.normalize_article(entry, feed_source, default_category)

                if normalized_article.get('image_url'):
                    if normalized_article.get('url'):
                        article_hash = normalized_article.get('sha256_hash')
                        if article_hash and not self.check_duplicate(article_hash):
                            article = Article(
                                title=normalized_article.get('title')[:255] if normalized_article.get('title') else None,
                                author=normalized_article.get('author')[:100] if normalized_article.get('author') else None,
                                source=normalized_article.get('source')[:100] if normalized_article.get('source') else None,
                                url=normalized_article.get('url'),
                                content=normalized_article.get('content'),
                                published_date=normalized_article.get('published_date'),
                                image_url=normalized_article.get('image_url'),
                                description=normalized_article.get('description'),
                                source_name=normalized_article.get('source_name')[:255] if normalized_article.get('source_name') else None,
                                category=normalized_article.get('category'),
                                sha256_hash=article_hash,
                            )
                            try:
                                article.save()
                                self.stdout.write(self.style.SUCCESS(f"Stored: {article.title[:50]}... from {feed_source} (Category: {article.category})"))
                            except Exception as e:
                                self.stderr.write(self.style.ERROR(f"Error saving from {feed_source}: {e}"))
                        else:
                            self.stdout.write(self.style.WARNING(f"Skipping duplicate: {normalized_article.get('url')}"))
                    else:
                        self.stdout.write(self.style.WARNING("No URL found, skipping."))
                else:
                    self.stdout.write(self.style.WARNING("Skipping article due to missing image URL."))

        except requests.exceptions.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Error fetching '{rss_url}': {e}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error processing '{rss_url}': {e}"))

    def handle(self, *args, **options):
        active_feeds = RSSFeed.objects.filter(is_active=True)
        self.stdout.write(self.style.SUCCESS(f'Found {active_feeds.count()} active RSS feeds.'))

        for feed in active_feeds:
            feed_name = feed.name
            feed_url = feed.url
            feed_source_name = feed.source_name
            feed_category = feed.category

            # self.stdout.write(self.style(f'Processing feed: {feed_name} ({feed_url})'))
            # self.stdout.write(self.style(f'  Source Name (Model): {feed_source_name}'))
            # self.stdout.write(self.style(f'  Category (Model): {feed_category}'))

            self.process_feed(feed)

        self.stdout.write(self.style.SUCCESS('Finished processing RSS feeds.'))