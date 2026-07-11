from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255) 
    author = models.CharField(max_length=100, blank=True, null=True)  
    source = models.CharField(max_length=100, blank=True, null=True) 
    url = models.URLField(unique=True) 
    content = models.TextField(blank=True, null=True)  
    published_date = models.DateTimeField(blank=True, null=True) 
    added_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)  
    description = models.TextField(blank=True, null=True)  
    source_name = models.CharField(max_length=255, blank=True, null=True) 
    category = models.CharField(max_length=100, blank=True, null=True)  
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
