# -*- coding: utf-8 -*-
from org.tools import *
from blogs.models import BlogArticle, BlogComment, BlogCategory

class ArticleForm(forms.ModelForm):
	class Meta:
		model = BlogArticle
		fields = ['title', 'category', 'tags', 'text']

@login_required
def delete_article_view(request, pk_text):
	article=get_object_or_404(BlogArticle, pk=pk_text)
	if checkf(lambda: request.user.lawyer==article.author):
		article.delete()
		message(request, u'文章删除成功')
	else:
		message(request, u'文章删除失败')
	return redirect('blogs:index', pk_lawyer=article.author.id)

@login_required
def edit_article_view(request, pk_text):
	article=get_object_or_404(BlogArticle, pk=pk_text)
	if request.method=='POST':
		if checkf(lambda: request.user.lawyer==article.author):
			form=ArticleForm(request.POST, instance=article)
			form.save()
			message(request, u'文章编辑成功')
		else:
			message(request, u'文章编辑失败')
		return redirect('blogs:index', pk_lawyer=article.author.id)
	else: 
		return response(request, 'blogs/edit.html', 
			article_edit=ArticleForm(instance=article),
			article=article)	

@login_required
def new_article_view(request):
	if request.method=='POST':
		try:
			BlogArticle.objects.create(
				author=request.user.lawyer,
				title=request.POST['title'],
				category=BlogCategory.objects.get(id=request.POST['category']),
				tags=request.POST['tags'],
				text=request.POST['text']
			).save()
		except BlogCategory.DoesNotExist, e: message(request, u'该分类不存在')
		except ObjectDoesNotExist, e: 
			message(request, u'该律师不存在')
			return redirect('index:index')
		else: message(request, u'文章创建成功')
		return redirect('blogs:index', pk_lawyer=request.user.lawyer.id)
	else: 
		return response(request, 'blogs/new.html', 
			article_create=ArticleForm())

def home_view(request):
	try:
		return response(request, 'blogs/index.html', 
			is_master=True,
			categories=BlogCategory.objects.filter(user=request.user.lawyer),
			latest_blogs_list=BlogArticle.objects.filter(author=request.user.lawyer.id).order_by('-publish_date'))
	except ObjectDoesNotExist, e: raise Http404

def index_view(request, pk_lawyer):
	return response(request, 'blogs/index.html', 
		is_master=checkf(lambda: request.user.lawyer.id==int(pk_lawyer)),
		categories=BlogCategory.objects.filter(user=request.user.lawyer),
		latest_blogs_list=BlogArticle.objects.filter(author=pk_lawyer).order_by('-publish_date'))

def detail_view(request, pk_text):
	article=get_object_or_404(BlogArticle, pk=pk_text)
	return response(request, 'blogs/detail.html', 
		is_master=checkf(lambda: request.user.lawyer==article.author),
		article=article,
		comments=BlogComment.objects.filter(article_id=pk_text))

@login_required
def new_comment_view(request, pk_text):
	if request.method=='POST':
		article=get_object_or_404(BlogArticle, pk=pk_text)
		BlogComment.objects.create( 
			user=request.user, 
			article=article,
			text=request.POST['txt_comment']
		).save()
		return redirect('blogs:text', pk_text=article.id)
	else: raise Http404

@login_required
def categories_view(request):
	try: 
		return response(request, 'blogs/categories.html', 
			categories=BlogCategory.objects.filter(user=request.user.lawyer))
	except ObjectDoesNotExist, e: raise Http404

