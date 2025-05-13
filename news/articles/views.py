from django.shortcuts import render
from rest_framework import generics
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home_view(request):
    return render(request, 'home/home.html')


class ArticleList(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all().order_by('?', '-published_date', '-added_date')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = request.GET.get('page')
        paginator = Paginator(queryset, 10)  # Show 10 articles per page (you can adjust this)

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        serializer = self.serializer_class(articles, many=True)
        return Response({
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': articles.number,
            'next': articles.has_next() and articles.next_page_number(),
            'previous': articles.has_previous() and articles.previous_page_number(),
            'results': serializer.data
        })



class ArticleListPagination(PageNumberPagination):
    page_size = 10



# @api_view(['GET'])
# def article_list_by_keyword(request):
#     """
#     API endpoint to retrieve a paginated list of articles filtered by a keyword.
#     """
#     queryset = Article.objects.all().order_by('?') # Default to random ordering
#     keyword = request.query_params.get('q', None)
#     print(f"Keyword: {keyword}")
#     if keyword:
#         queryset = queryset.filter(
#             Q(title__icontains=keyword) |
#             Q(description__icontains=keyword) |
#             Q(content__icontains=keyword)
#         )

#     paginator = ArticleListPagination()
#     paginated_queryset = paginator.paginate_queryset(queryset, request)
#     serializer = ArticleSerializer(paginated_queryset, many=True)
#     return paginator.get_paginated_response(serializer.data)




class ArticleListByCategory(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self, category):
        print(f"Category: {category}")
        return Article.objects.filter(category=category)
    

    def list(self, request, category=None, *args, **kwargs):
        if not category:
            return Response({"error": "Category parameter is required."}, status=400)
        
        queryset = self.get_queryset(category)
        
        page = request.GET.get('page')
        paginator = Paginator(queryset, 10)  # Show 10 articles per page (you can adjust this)

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        serializer = self.serializer_class(articles, many=True)
    
    
        return Response({
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': articles.number,
            'next': articles.has_next() and articles.next_page_number(),
            'previous': articles.has_previous() and articles.previous_page_number(),
            'results': serializer.data
        })
    

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
from django.urls import reverse
from urllib.parse import urlencode
from fuzzywuzzy import fuzz
from django.db.models import Value
from django.db.models.functions import Greatest

@api_view(['GET'])
def article_list_by_keyword(request):
    query = request.GET.get('q')

    if not query:
        return Response({"error": "Please provide a search keyword in the 'q' parameter."}, status=400)


    articles = Article.objects.all()
    results = []

    for article in articles:
        title_sim = fuzz.partial_ratio(query.lower(), article.title.lower())
        desc_sim = fuzz.partial_ratio(query.lower(), article.description.lower())
        content_sim = fuzz.partial_ratio(query.lower(), article.content.lower())

        max_similarity = max(title_sim, desc_sim, content_sim)

        if max_similarity > 70:  # Threshold
            results.append(article)

    
    

    page = request.GET.get('page')
    paginator = Paginator(results, 10)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    serializer = ArticleSerializer(articles, many=True)

    

    return Response({
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': articles.number,
        'next': articles.has_next() and articles.next_page_number(),
        'previous': articles.has_previous() and articles.previous_page_number(),
        'results': serializer.data
    })