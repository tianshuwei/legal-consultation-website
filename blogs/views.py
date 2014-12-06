# -*- coding: utf-8 -*-
from org.tools import *
from accounts.models import Lawyer
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
		except: message(request, u'文章创建失败')
		else: message(request, u'文章创建成功')
		return redirect('blogs:index', pk_lawyer=request.user.lawyer.id)
	else: 
		return response(request, 'blogs/new.html', 
			article_create=ArticleForm())

def home_view(request):
	try: return redirect('blogs:index', pk_lawyer=request.user.lawyer.id)
	except ObjectDoesNotExist, e: raise Http404

def index_view(request, pk_lawyer):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	return response(request, 'blogs/index.html', 
		lawyer=lawyer,
		is_master=checkf(lambda: request.user.lawyer==lawyer),
		categories=BlogCategory.objects.filter(lawyer=pk_lawyer),
		latest_blogs_list=BlogArticle.objects.filter(author=pk_lawyer).order_by('-publish_date'))

def index_category_view(request, pk_lawyer, pk_category):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	category=get_object_or_404(BlogCategory, pk=pk_category)
	return response(request, 'blogs/index_category.html', 
		lawyer=lawyer,
		is_master=checkf(lambda: request.user.lawyer==lawyer),
		category=category,
		latest_blogs_list=BlogArticle.objects.filter(author=pk_lawyer).filter(category=category).order_by('-publish_date'))

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
			lawyer=request.user, 
			article=article,
			text=request.POST['txt_comment']
		).save()
		return redirect('blogs:text', pk_text=article.id)
	else: raise Http404

@login_required
def categories_view(request):
<<<<<<< HEAD
	try: 
		return response(request, 'blogs/categories.html', 
			categories=BlogCategory.objects.filter(lawyer=request.user.lawyer))
	except ObjectDoesNotExist, e: raise Http404
=======
	if request.method=='POST':
		try: 
			BlogCategory.objects.create(
				lawyer=request.user.lawyer,
				name=request.POST['name']
			).save()
		except ObjectDoesNotExist, e: message(request, u'新分类创建失败')
		except: message(request, u'新分类创建失败')
		else: message(request, u'新分类创建成功')
		return redirect('blogs:categories')
	else:
		try: 
			return response(request, 'blogs/categories.html', 
				categories=BlogCategory.objects.filter(lawyer=request.user.lawyer))
		except ObjectDoesNotExist, e: raise Http404
>>>>>>> temp

@login_required
def delete_category_view(request, pk_category):
	category=get_object_or_404(BlogCategory, pk=pk_category)
	if checkf(lambda: request.user.lawyer==category.lawyer):
		category.delete()
		message(request, u'分类删除成功')
	else:
		message(request, u'分类删除失败')
	return redirect('blogs:categories')

@login_required
def rename_category_view(request, pk_category):
	category=get_object_or_404(BlogCategory, pk=pk_category)
	if checkf(lambda: request.user.lawyer==category.lawyer):
		category.name=request.POST['name']
		category.save()
		message(request, u'分类重命名成功')
	else:
		message(request, u'分类重命名失败')
	return redirect('blogs:categories')
