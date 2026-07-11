from django.core.management.base import BaseCommand
from articles.models import RSSFeed, Article
import requests
import feedparser
import hashlib
from datetime import datetime, timezone
from bs4 import BeautifulSoup

class Command(BaseCommand):
    help = 'Fetches and processes articles from RSS feeds'



    def normalize_article(self ,entry,source, category):
        try:
        
            title = entry.get('title', '').strip()

            
            url = entry.get('link') or entry.get('id') or ''
            url = url.strip()

            description = entry.get('summary', '').strip()
            soup = BeautifulSoup(description, 'html.parser')

            
            for img_tag in soup.find_all('img'):
                img_tag.decompose()

            
            cleaned_description = soup.get_text().strip()

           
            content = ''
            if 'content' in entry:
                if isinstance(entry['content'], list) and len(entry['content']) > 0:
                    content = entry['content'][0].get('value', '').strip()
                elif isinstance(entry['content'], dict):
                    content = entry['content'].get('value', '').strip()
            if not content:
                content = cleaned_description

           
            published_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            

           
            image_url = ''
            media_content = entry.get('media_content', [])
            if isinstance(media_content, list) and media_content:
                image_url = media_content[0].get('url', '')

            if not image_url and 'media_thumbnail' in entry:
                thumb = entry['media_thumbnail']
                if isinstance(thumb, list) and thumb:
                    image_url = thumb[0].get('url', '')

            if not image_url and 'enclosures' in entry:
                enclosures = entry['enclosures']
                if isinstance(enclosures, list) and enclosures:
                    for enc in enclosures:
                        if 'image' in enc.get('type', ''):
                            image_url = enc.get('href', '')
                            break

           
            if not image_url:
                soup = BeautifulSoup(content or description, 'html.parser')
                img_tag = soup.find('img')
                if img_tag and img_tag.get('src'):
                    image_url = img_tag['src']

           
            if not image_url or not image_url.startswith('http'):
                return None

          
            hash_input = f"{title}{description}{url}".encode('utf-8')
            hash_val = hashlib.sha256(hash_input).hexdigest()

          
            return {
                'title': title,
                'url': url,
                'content': content,
                'description': cleaned_description,
                'source_name': source,
                'category': category,
                'published_date': published_date,
                'image_url': image_url,
                'sha256_hash': hash_val
            }

        except Exception:
            return None


    def check_duplicate(self, article_hash):
        """Checks if an article with the given SHA256 hash already exists."""
        return Article.objects.filter(sha256_hash=article_hash).exists()


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

            

            self.process_feed(feed)

        self.stdout.write(self.style.SUCCESS('Finished processing RSS feeds.'))