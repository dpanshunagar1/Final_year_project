# news/urls.py
from django.contrib import admin
from django.urls import path, include
from articles.views import ArticleList,ArticleDetail,home_view,article_list_by_keyword



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Home view
    path('api/articles/', ArticleList.as_view(), name='article-list'),
    path('api/articles/<int:pk>/', ArticleDetail.as_view(), name='article-detail'),
    path('articles/search/', article_list_by_keyword, name='article-list-by-keyword'),
]

