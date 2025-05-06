from django.contrib import admin
from .models import Article,RSSFeed

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'source_name', 'category', 'published_date')
    list_filter = ('category', 'source_name', 'published_date')
    search_fields = ('title', 'author', 'source_name', 'category')
    actions = ['update_category', 'update_source_name']

    def update_category(self, request, queryset):
        # Action to update the category of selected articles
        queryset.update(category='technology')
        self.message_user(request, "Category updated successfully.")

    def update_source_name(self, request, queryset):
        # Action to update the source name of selected articles
        queryset.update(source_name='Updated Source')
        self.message_user(request, "Source name updated successfully.")

    update_category.short_description = 'Update category of selected articles'
    update_source_name.short_description = 'Update source name of selected articles'

admin.site.register(Article, ArticleAdmin)
admin.site.register(RSSFeed)