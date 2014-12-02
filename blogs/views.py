from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django import forms
from django.views import generic
from blogs.models import BlogArticle, BlogComment, BlogCategory

def new_article_view(request):
    raise Http404

class IndexView(generic.ListView):
	template_name = 'blogs/index.html'
	context_object_name = 'latest_blogs_list'

	def get_queryset(self):
		return BlogArticle.objects.filter(author=self.kwargs['pk']).order_by('-publish_date')

class DetailView(generic.DetailView):
	model = BlogArticle
	template_name = 'blogs/detail.html'
	context_object_name = 'article'

def categories_view(request):
    raise Http404


