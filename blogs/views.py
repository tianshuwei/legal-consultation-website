from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django import forms
from django.views import generic
from blogs.models import BlogArticle, BlogComment, BlogCategory

# def index_view(request, pk):
# 	template = loader.get_template('accounts/register.html')
# 	context = RequestContext(request, {
# 		'register_form':register_form
# 	})
# 	return HttpResponse(template.render(context))

def new_article_view(request):
    raise Http404

def index_view(request, pk):
    template = loader.get_template('blogs/index.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

class IndexView(generic.ListView):
	template_name = 'blogs/index.html'
	context_object_name = 'latest_blogs_list'

	def get_queryset(self):
		return BlogArticle.objects.order_by('-publish_date')

def text_view(request, pk):
    raise Http404

def categories_view(request):
    raise Http404


