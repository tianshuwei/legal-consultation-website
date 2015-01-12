# -*- coding: utf-8 -*-
from org.tools import *
from accounts.models import Lawyer
from blogs.models import BlogArticle, BlogComment, BlogCategory, BlogSettings

class ArticleForm(forms.ModelForm):
	class Meta:
		model = BlogArticle
		fields = ['title', 'category', 'tags', 'text']
		labels = {
			'title' : u'标题',
			'category' : u'分类',
			'tags' : u'标签',
			'text' : u'正文',
		}

@login_required
def delete_article_view(request, pk_text): # TODO use post
	article=get_object_or_404(BlogArticle, pk=pk_text)
	if checkf(lambda: request.user.lawyer==article.author):
		article.delete()
		messages.success(request, u'文章删除成功')
	else:
		messages.error(request, u'文章删除失败')
	return redirect('blogs:index', pk_lawyer=article.author.id)

@login_required
def edit_article_view(request, pk_text):
	article=get_object_or_404(BlogArticle, pk=pk_text)
	if request.method=='POST':
		rec=recorded(request,'blogs:new_article')
		if checkf(lambda: request.user.lawyer==article.author):
			form=ArticleForm(request.POST, instance=article)
			form.save()
			messages.success(request, rec(u'文章编辑成功'))
		else:
			messages.error(request, rec(u'文章编辑失败'))
		return redirect('blogs:index', pk_lawyer=article.author.id)
	else: 
		return response(request, 'blogs/edit.html', 
			article_edit=ArticleForm(instance=article),
			article=article)	

@login_required
def new_article_view(request):
	if request.method=='POST':
		rec=recorded(request,'blogs:new_article')
		try:
			BlogArticle.objects.create(
				author=request.user.lawyer,
				title=request.POST['title'],
				category=BlogCategory.objects.get(id=request.POST['category']),
				tags=request.POST['tags'],
				text=request.POST['text']
			).save()
		except BlogCategory.DoesNotExist, e: 
			messages.error(request, rec(u'该分类不存在'))
		except ObjectDoesNotExist, e: 
			messages.error(request, rec(u'该律师不存在'))
			return redirect('index:index')
		except: messages.error(request, rec(u'文章创建失败'))
		else: messages.success(request, rec(u'文章创建成功'))
		return redirect('blogs:index', pk_lawyer=request.user.lawyer.id)
	else: 
		return response(request, 'blogs/new.html', 
			article_create=ArticleForm())

def home_view(request):
	try: return redirect('blogs:index', pk_lawyer=request.user.lawyer.id)
	except ObjectDoesNotExist, e: raise Http404

def list_view(request):
	return response(request, 'blogs/list.html',
		lawyers=Lawyer.objects.all())

def index_view(request, pk_lawyer):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	blogsettings, created=BlogSettings.objects.get_or_create(lawyer=lawyer)
	if blogsettings.state==1: raise Http404 # Blog disabled
	return response(request, 'blogs/index.html', 
		lawyer=lawyer,
		is_master=checkf(lambda: request.user.lawyer==lawyer),
		categories=lawyer.blogcategory_set.filter(state__lte=0),
		latest_blogs_list=paginated(lambda: request.GET.get('page'), blogsettings.items_per_page, 
			lawyer.blogarticle_set.filter(category__isnull=False).order_by('-publish_date')))

def index_category_view(request, pk_lawyer, pk_category):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	category=get_object_or_404(BlogCategory, pk=pk_category)
	blogsettings, created=BlogSettings.objects.get_or_create(lawyer=lawyer)
	if blogsettings.state==1: raise Http404 # Blog disabled
	return response(request, 'blogs/index_category.html', 
		lawyer=lawyer,
		is_master=checkf(lambda: request.user.lawyer==lawyer),
		category=category,
		latest_blogs_list=paginated(lambda: request.GET.get('page'), blogsettings.items_per_page, 
			lawyer.blogarticle_set.filter(category=category).order_by('-publish_date')))

def detail_view(request, pk_text):
	article=get_object_or_404(BlogArticle, pk=pk_text)
	return response(request, 'blogs/detail.html', 
		is_master=checkf(lambda: request.user.lawyer==article.author),
		article=article,
		comments=article.blogcomment_set.order_by('-publish_date'))

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
	if request.method=='POST':
		try: 
			category=BlogCategory.objects.create(
				lawyer=request.user.lawyer,
				name=request.POST['name']
			)
			category.save()
		except ObjectDoesNotExist, e: 
			messages.error(request, u'新分类创建失败')
			return response_auto(request, { 'success': False }, 'blogs:categories')
		except: 
			messages.error(request, u'新分类创建失败')
			return response_auto(request, { 'success': False }, 'blogs:categories')
		else: 
			messages.success(request, u'新分类创建成功')
			return response_auto(request, { 
				'success': True, 
				'pk': category.id, 
				'name':category.name, 
				'href': url_of('blogs:index_category', pk_lawyer=category.lawyer.id, pk_category=category.id),
				'edit_href': url_of('blogs:rename_category', pk_category=category.id),
				'del_href': url_of('blogs:delete_category', pk_category=category.id),
			}, 'blogs:categories')
	else:
		try: 
			return response(request, 'blogs/categories.html', 
				categories=request.user.lawyer.blogcategory_set.all())
		except ObjectDoesNotExist, e: raise Http404

@login_required
def delete_category_view(request, pk_category):
	category=get_object_or_404(BlogCategory, pk=pk_category)
	if checkf(lambda: request.user.lawyer==category.lawyer):
		category.remove()
		messages.success(request, u'分类删除成功')
		return response_auto(request, { 'success': True }, 'blogs:categories')
	else:
		messages.error(request, u'分类删除失败')
		return response_auto(request, { 'success': False }, 'blogs:categories')

@login_required
def rename_category_view(request, pk_category):
	category=get_object_or_404(BlogCategory, pk=pk_category)
	if checkf(lambda: request.user.lawyer==category.lawyer):
		category.name=request.POST['name']
		category.save()
		messages.success(request, u'分类重命名成功')
		return response_auto(request, { 'success': True, 'pk':category.id, 'name':category.name  }, 'blogs:categories')
	else:
		messages.error(request, u'分类重命名失败')
		return response_auto(request, { 'success': False }, 'blogs:categories')
