from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.views import generic
from django.contrib.auth.decorators import login_required
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

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		context['comments'] = BlogComment.objects.filter(article_id=self.object.id)
		return context

@login_required
def new_comment_view(request, pk):
	p = get_object_or_404(BlogArticle, pk=pk)
	comment = BlogComment.objects.create(text=request.POST['txt_comment'], user=request.user, article=p)
	comment.save()
	return HttpResponseRedirect(reverse('blogs:text', args=(p.id,)))

@login_required
def categories_view(request):
	try:
		return HttpResponseRedirect(reverse('blogs:index',kwargs={'pk':request.user.lawyer.id}))
	except ObjectDoesNotExist, e:
		raise Http404

