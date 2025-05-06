# news/urls.py
from django.contrib import admin
from django.urls import path, include
from articles.views import ArticleList,home_view,article_list_by_keyword,ArticleListByCategory



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Home view
    path('api/articles/', ArticleList.as_view(), name='article-list'),
    path('articles/search/', article_list_by_keyword, name='article-list-by-keyword'),
    path('api/articles/category/<str:category>/', ArticleListByCategory.as_view(), name='article-list-by-category'),
]

