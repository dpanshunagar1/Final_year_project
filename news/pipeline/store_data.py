# articles/models.py (assuming your Django app is named 'articles')

from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(unique=True)
    published = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    authors = models.JSONField(null=True, blank=True)  # Store authors as a JSON array
    sha256_hash = models.CharField(max_length=64, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published']