from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)  # Article title
    author = models.CharField(max_length=100, blank=True, null=True)  # Author's name
    source = models.CharField(max_length=100, blank=True, null=True)  # Source of the article
    url = models.URLField(unique=True)  # URL of the article
    content = models.TextField(blank=True, null=True)  # Main content of the article
    published_date = models.DateTimeField(blank=True, null=True)  # Publication date
    added_date = models.DateTimeField(auto_now_add=True)  # Date the article was added to the database
    image_url = models.URLField(blank=True, null=True)  # URL of the article image
    description = models.TextField(blank=True, null=True)  # Description of the article
    source_name = models.CharField(max_length=255, blank=True, null=True)  # Name of the source
    category = models.CharField(max_length=100, blank=True, null=True)  # Category of the article
    sha256_hash = models.CharField(max_length=64, unique=True, blank=True, null=True, db_index=True)  

    def __str__(self):
        return self.title



class RSSFeed(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Name of the feed (e.g., 'The Hindu National')")
    url = models.URLField(unique=True, help_text="URL of the RSS feed")
    is_active = models.BooleanField(default=True, help_text="Whether this feed should be processed")
    source_name = models.CharField(max_length=255, blank=True, help_text="The name of the source (e.g., 'The Hindu'). If blank, it will try to fetch from the feed.")
    category = models.CharField(max_length=100, blank=True, help_text="The default category for articles from this feed (e.g., 'World', 'Sports').")

    def __str__(self):
        return self.name
