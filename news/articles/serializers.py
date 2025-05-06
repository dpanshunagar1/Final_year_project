# news/articles/serializers.py
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'  # Or specify the fields you want to expose
        # Example of specific fields:
        # fields = ['id', 'title', 'author', 'source_name', 'url', 'description', 'published_date', 'category']