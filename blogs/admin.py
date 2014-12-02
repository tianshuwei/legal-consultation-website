from django.contrib import admin
from blogs.models import BlogArticle, BlogComment, BlogCategory

class CommentInline(admin.TabularInline):
	model = BlogComment
	verbose_name_plural = 'comments'

class BlogArticleAdmin(admin.ModelAdmin):
	inlines = [CommentInline]

admin.site.register(BlogArticle, BlogArticleAdmin)
admin.site.register(BlogCategory)
