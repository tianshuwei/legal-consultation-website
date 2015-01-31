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
def delete_article_view(request, pk_text):
	article=get_object_or_404(BlogArticle, pk=pk_text)
	if request.method=='POST':
		rec=recorded(request,'blogs:delete_article')
		if checkf(lambda: request.user.lawyer==article.author):
			article.remove()
			messages.success(request, u'文章删除成功')
			rec.success(u'{0} 删除文章 {1} 成功'.format(request.user.username, article.title))
			return response_auto(request, { 'success': True }, 'blogs:index', pk_lawyer=article.author.id)
		else:
			messages.error(request, u'文章删除失败')
			rec.error(u'{0} 删除文章 {1} 失败'.format(request.user.username, article.title))
			return response_auto(request, { 'success': False }, 'blogs:index', pk_lawyer=article.author.id)
	else: raise Http404

@login_required # [LiveTest]
def edit_article_view(request, pk_text):
	article=get_object_or_404(BlogArticle, pk=pk_text)
	if request.method=='POST': 
		rec=recorded(request,'blogs:edit_article')
		if checkf(lambda: request.user.lawyer==article.author):
			form=ArticleForm(request.POST, instance=article)
			form.save()
			messages.success(request, u'文章编辑成功')
			rec.success(u'{0} 编辑文章 {1} 成功'.format(request.user.username, article.title)) # [LiveTest]
		else:
			messages.error(request, u'文章编辑失败')
			rec.error(u'{0} 编辑文章 {1} 失败'.format(request.user.username, article.title))
		return redirect('blogs:index', pk_lawyer=article.author.id)
	else: 
		return response(request, 'blogs/edit.html', 
			article_edit=ArticleForm(instance=article),
			article=article)	

@login_required # [LiveTest]
def new_article_view(request):
	if request.method=='POST': # [LiveTest]
		rec=recorded(request,'blogs:new_article')
		try:
			article=BlogArticle.objects.create(
				author=request.user.lawyer,
				title=request.POST['title'],
				category=BlogCategory.objects.get(id=request.POST['category']),
				tags=request.POST['tags'],
				text=request.POST['text']
			)
			article.save()
		except BlogCategory.DoesNotExist, e: 
			messages.error(request, u'该分类不存在')
			rec.error(u'{0} 创建文章失败，因为分类不存在'.format(request.user.username))
		except ObjectDoesNotExist, e: 
			messages.error(request, u'该律师不存在')
			rec.error(u'{0} 创建文章失败，因为律师不存在'.format(request.user.username))
			return redirect('index:index')
		except: 
			messages.error(request, u'文章创建失败')
			rec.error(u'{0} 创建文章失败'.format(request.user.username))
		else: 
			messages.success(request, u'文章创建成功')
			rec.success(u'{0} 创建文章 {1} 成功'.format(request.user.username, article.title)) # [LiveTest]
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

def categories_mod_view(request, pk_lawyer):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	return response(request, 'blogs/category.mod.html',
		is_master=checkf(lambda: request.GET['e']=='True'),
		categories=lawyer.blogcategory_set.get_public_categories())

def index_view(request, pk_lawyer):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	blogsettings, created=BlogSettings.objects.get_or_create(lawyer=lawyer)
	if blogsettings.state==1: raise Http404 # Blog disabled
	return response(request, 'blogs/index.html', lawyer=lawyer,
		is_master=checkf(lambda: request.user.lawyer==lawyer),
		articles=paginated(lambda: request.GET.get('page'), blogsettings.items_per_page, 
			lawyer.blogarticle_set.get_public_articles()))

def index_category_view(request, pk_category):
	category=get_object_or_404(BlogCategory, pk=pk_category)
	blogsettings, created=BlogSettings.objects.get_or_create(lawyer=category.lawyer)
	if blogsettings.state==1: raise Http404 # Blog disabled
	return response(request, 'blogs/index_category.html', category=category,
		is_master=checkf(lambda: request.user.lawyer==category.lawyer),
		articles=paginated(lambda: request.GET.get('page'), blogsettings.items_per_page, 
			category.blogarticle_set.get_public_articles()))

def search_view(request, pk_lawyer):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	blogsettings, created=BlogSettings.objects.get_or_create(lawyer=lawyer)
	if blogsettings.state==1: raise Http404 # Blog disabled
	if 'q' not in request.GET: raise Http404
	else: query=request.GET['q']
	return response(request, 'blogs/search.html', lawyer=lawyer, query=query, 
		articles=paginated(lambda: request.GET.get('page'), blogsettings.items_per_page, lawyer.blogarticle_set.search(query)))

def detail_view(request, pk_text):
	article=get_object_or_404(BlogArticle, pk=pk_text)
	return response(request, 'blogs/detail.html', article=article,
		is_master=checkf(lambda: request.user.lawyer==article.author),
		comments=article.blogcomment_set.order_by('-publish_date'))

@login_required # [LiveTest] [UnitTest]
def new_comment_view(request, pk_text):
	if request.method=='POST':
		rec=recorded(request,'blogs:new_article')
		try:
			article=BlogArticle.objects.get(id=pk_text)
		except BlogArticle.DoesNotExist, e: # [UnitTest]
			rec.error(u'{0} 评论文章失败'.format(request.user.username))
			raise Http404
		BlogComment.objects.create( 
			user=request.user, 
			article=article,
			text=request.POST['txt_comment']
		).save()
		rec.success(u'{0} 评论文章 {1} 成功'.format(request.user.username, article.title)) # [LiveTest] [UnitTest]
		return redirect('blogs:text', pk_text=article.id)
	else: raise Http404

def recent_comments_mod_view(request, pk_lawyer):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	return response(request, 'blogs/recent_comments.mod.html',
		recent_comments=BlogComment.objects.get_recent_comments(lawyer))

@login_required # [UnitTest]
def categories_view(request):
	if request.method=='POST':
		rec=recorded(request,'blogs:categories')
		try: 
			with transaction.atomic():
				category=BlogCategory.objects.create(
					lawyer=request.user.lawyer,
					name=request.POST['name']
				)
				category.save()
		except ObjectDoesNotExist, e: # [UnitTest]
			messages.error(request, u'新分类创建失败')
			rec.error(u'{0} 新分类创建失败'.format(request.user.username))
			return response_auto(request, { 'success': False }, 'blogs:categories')
		except: # [UnitTest]
			messages.error(request, u'新分类创建失败')
			rec.error(u'{0} 新分类创建失败'.format(request.user.username))
			return response_auto(request, { 'success': False }, 'blogs:categories')
		else: # [UnitTest]
			messages.success(request, u'新分类创建成功')
			rec.success(u'{0} 新分类 {1} 创建成功'.format(request.user.username,category.name)) # [UnitTest]
			return response_auto(request, { 
				'success': True, 
				'pk': category.id, 
				'name':category.name, 
				'href': url_of('blogs:index_category', pk_lawyer=category.lawyer.id, pk_category=category.id),
				'edit_href': url_of('blogs:rename_category', pk_category=category.id),
				'del_href': url_of('blogs:delete_category', pk_category=category.id),
			}, 'blogs:categories')
	else: raise Http404

@login_required # [UnitTest]
def delete_category_view(request, pk_category):
	if request.method=='POST':
		rec=recorded(request,'blogs:delete_category')
		try:
			category=BlogCategory.objects.get(id=pk_category)
		except BlogCategory.DoesNotExist, e: # [UnitTest]
			rec.error(u'{0} 删除分类失败，因为分类不存在'.format(request.user.username))
			raise Http404
		if checkf(lambda: request.user.lawyer==category.lawyer): # [UnitTest]
			category.remove()
			messages.success(request, u'分类删除成功') 
			rec.success(u'{0} 删除分类 {1} 成功'.format(request.user.username,category.name))
			return response_auto(request, { 'success': True }, 'blogs:categories')
		else: # [UnitTest]
			messages.error(request, u'分类删除失败')
			rec.error(u'{0} 删除分类 {1} 失败，因为权限不足'.format(request.user.username,category.name))
			return response_auto(request, { 'success': False }, 'blogs:categories')
	else: raise Http404

@login_required # [UnitTest]
def rename_category_view(request, pk_category):
	if request.method=='POST':
		rec=recorded(request,'blogs:rename_category')
		try:
			category=BlogCategory.objects.get(id=pk_category)
		except BlogCategory.DoesNotExist, e: # [UnitTest]
			rec.error(u'{0} 重命名分类失败，因为分类不存在'.format(request.user.username))
			raise Http404
		if checkf(lambda: request.user.lawyer==category.lawyer): # [UnitTest]
			category.name=request.POST['name']
			category.save()
			messages.success(request, u'分类重命名成功')
			rec.success(u'{0} 重命名分类 {1} 成功'.format(request.user.username,category.name))
			return response_auto(request, { 'success': True, 'pk':category.id, 'name':category.name  }, 'blogs:categories')
		else: # [UnitTest]
			messages.error(request, u'分类重命名失败')
			rec.error(u'{0} 重命名分类 {1} 失败，因为权限不足'.format(request.user.username,category.name))
			return response_auto(request, { 'success': False }, 'blogs:categories')
	else: raise Http404
