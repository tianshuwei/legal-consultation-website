# -*- coding: utf-8 -*-
from org.tools import *
from org.widgets import BootstrapWYSIWYG, BlogCategorySelect
from accounts.models import Lawyer, Activity
from blogs.models import BlogArticle, BlogComment, BlogCategory, BlogSettings

class ArticleForm(forms.ModelForm):
	class Meta:
		model = BlogArticle
		fields = ['title', 'category', 'tags', 'text']
		widgets = {
			'category': BlogCategorySelect,
			'text': BootstrapWYSIWYG(attrs={'class': 'form-control', 'id': 'editor'}), 
		}

@login_required # [UnitTest]
def delete_article_view(request, pk_text):
	article=get_object_or_404(BlogArticle, pk=pk_text)
	if request.method=='POST':
		rec=recorded(request,'blogs:delete_article')
		if checkf(lambda: request.user.lawyer==article.author):
			article.remove()
			messages.success(request, u'文章删除成功') # [UnitTest]
			rec.success(u'{0} 删除文章 {1} 成功'.format(request.user.username, article.title))
			return response_auto(request, { 'success': True }, 'blogs:index', pk_lawyer=article.author.id)
		else:
			handle_illegal_access(request, False)
			messages.error(request, u'文章删除失败') # [UnitTest]
			rec.error(u'{0} 删除文章 {1} 失败'.format(request.user.username, article.title))
			return response_auto(request, { 'success': False }, 'blogs:index', pk_lawyer=article.author.id)
	else: handle_illegal_access(request)

@login_required # [LiveTest] [UnitTest]
def edit_article_view(request, pk_text):
	article=get_object_or_404(BlogArticle, pk=pk_text)
	if request.method=='POST': 
		rec=recorded(request,'blogs:edit_article')
		if checkf(lambda: request.user.lawyer==article.author):
			form=ArticleForm(request.POST, instance=article)
			form.save()
			messages.success(request, u'文章编辑成功') # [LiveTest] [UnitTest]
			rec.success(u'{0} 编辑文章 {1} 成功'.format(request.user.username, article.title))
		else:
			handle_illegal_access(request, False)
			messages.error(request, u'文章编辑失败') # [UnitTest]
			rec.error(u'{0} 编辑文章 {1} 失败'.format(request.user.username, article.title))
		return redirect('blogs:index', pk_lawyer=article.author.id)
	else: 
		return response(request, 'blogs/edit.html', 
			article_edit=ArticleForm(instance=article),
			article=article)	

@login_required # [LiveTest] [UnitTest]
def new_article_view(request):
	if request.method=='POST':
		rec=recorded(request,'blogs:new_article')
		try:
			with transaction.atomic():
				from org.antixss import antiXSS_BootstrapWYSIWYS as antixss
				article = ArticleForm(request.POST).save(commit=False)
				article.author = request.user.lawyer
				# article.publish_date = datetime.now()
				article.text = antixss(article.text, strip=True)
				article.save()
		except BlogCategory.DoesNotExist, e: 
			handle_illegal_access(request, False)
			messages.error(request, u'该分类不存在') # [UnitTest]
			rec.error(u'{0} 创建文章失败，因为分类不存在'.format(request.user.username))
			return response_jquery({ 'success': False, 'redirect': href('blogs:index', pk_lawyer=request.user.lawyer.id)})
		except ObjectDoesNotExist, e: 
			messages.error(request, u'该律师不存在') # [UnitTest]
			rec.error(u'{0} 创建文章失败，因为律师不存在'.format(request.user.username))
			return response_jquery({ 'success': False, 'redirect': href('index:index')})
		except:
			logger.exception('Untestable')
			handle_illegal_access(request, False)
			messages.error(request, u'文章创建失败')
			rec.error(u'{0} 创建文章失败'.format(request.user.username))
			return response_jquery({ 'success': False, 'redirect': href('blogs:index', pk_lawyer=request.user.lawyer.id)})
		else: 
			messages.success(request, u'文章创建成功') # [LiveTest] [UnitTest]
			rec.success(u'{0} 创建文章 {1} 成功'.format(request.user.username, article.title)) # [LiveTest]
			Activity.objects.notify_new_blog_article(article)
			return response_jquery({ 'success': True, 'redirect': href('blogs:index', pk_lawyer=request.user.lawyer.id)})
	else: 
		return response(request, 'blogs/new.html', article_create=ArticleForm())

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

def favourite_posts_mod_view(request, pk_lawyer):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	return response(request, 'blogs/favourite_posts.mod.html',
		articles=lawyer.blogarticle_set.get_favourite_articles())

def chez(pk_lawyer):
	lawyer = get_object_or_404(Lawyer, pk=pk_lawyer)
	blogsettings = or404(lambda: BlogSettings.objects.get_blogsettings(lawyer))
	return lawyer, blogsettings

def index_view(request, pk_lawyer):
	lawyer, blogsettings=chez(pk_lawyer)
	return response(request, 'blogs/index.html', lawyer=lawyer,
		is_master=checkf(lambda: request.user.lawyer==lawyer),
		articles=paginated(lambda: request.GET.get('page'), blogsettings.items_per_page, 
			lawyer.blogarticle_set.get_public_articles()))

def index_category_view(request, pk_category):
	category=get_object_or_404(BlogCategory, pk=pk_category)
	blogsettings=or404(lambda: BlogSettings.objects.get_blogsettings(category.lawyer))
	return response(request, 'blogs/index_category.html', category=category,
		is_master=checkf(lambda: request.user.lawyer==category.lawyer),
		articles=paginated(lambda: request.GET.get('page'), blogsettings.items_per_page, 
			category.blogarticle_set.get_public_articles()))

def index_tag_view(request, pk_lawyer, tag):
	lawyer, blogsettings=chez(pk_lawyer)
	return response(request, 'blogs/index_tag.html', lawyer=lawyer, tag=tag,
		articles=paginated(lambda: request.GET.get('page'), blogsettings.items_per_page, 
			lawyer.blogarticle_set.get_public_articles_tagged(tag)))

def index_archive_view(request, pk_lawyer, year, month):
	lawyer, blogsettings=chez(pk_lawyer)
	return response(request, 'blogs/index_archive.html', lawyer=lawyer, 
		publish_date=datetime(int(year), int(month), 1),
		articles=paginated(lambda: request.GET.get('page'), blogsettings.items_per_page, 
			lawyer.blogarticle_set.get_archived_articles(year, month)))

def search_view(request, pk_lawyer, query=None):
	lawyer, blogsettings=chez(pk_lawyer)
	if query==None: query=or404(lambda: request.GET['q'])
	return response(request, 'blogs/search.html', lawyer=lawyer, query=query, 
		articles=paginated(lambda: request.GET.get('page'), blogsettings.items_per_page, lawyer.blogarticle_set.search(query)))

def detail_view(request, pk_text):
	article=get_object_or_404(BlogArticle, pk=pk_text)
	article.touch()
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
			handle_illegal_access(request)
		comment=BlogComment.objects.create( 
			user=request.user, 
			article=article,
			text=request.POST['txt_comment']
		)
		comment.save()
		rec.success(u'{0} 评论文章 {1} 成功'.format(request.user.username, article.title)) # [LiveTest] [UnitTest]
		Activity.objects.notify_new_blog_comment(article.author.user, comment)
		Activity.objects.profile_new_blog_comment(article.author.user, comment)
		return redirect('blogs:text', pk_text=article.id)
	else: handle_illegal_access(request)

def recent_comments_mod_view(request, pk_lawyer):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	return response(request, 'blogs/recent_comments.mod.html',
		recent_comments=BlogComment.objects.get_recent_comments(lawyer))

def tags_mod_view(request, pk_lawyer):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	return response(request, 'blogs/tags.mod.html', lawyer=lawyer,
		tags=BlogArticle.objects.get_tags(pk_lawyer))

def archives_mod_view(request, pk_lawyer):
	lawyer=get_object_or_404(Lawyer, pk=pk_lawyer)
	return response(request, 'blogs/archives.mod.html', lawyer=lawyer,
		archives=BlogArticle.objects.get_archives(pk_lawyer))

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
			handle_illegal_access(request, False)
			messages.error(request, u'新分类创建失败')
			rec.error(u'{0} 新分类创建失败'.format(request.user.username))
			return response_auto(request, { 'success': False }, 'blogs:categories')
		except: # Could be violation of integrity [UnitTest]
			handle_illegal_access(request, False)
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
				'href': url_of('blogs:index_category', pk_category=category.id),
				'edit_href': url_of('blogs:rename_category', pk_category=category.id),
				'del_href': url_of('blogs:delete_category', pk_category=category.id),
			}, 'blogs:categories')
	else: handle_illegal_access(request)

@login_required # [UnitTest]
def delete_category_view(request, pk_category):
	if request.method=='POST':
		rec=recorded(request,'blogs:delete_category')
		try:
			category=BlogCategory.objects.get(id=pk_category)
		except BlogCategory.DoesNotExist, e: # [UnitTest]
			rec.error(u'{0} 删除分类失败，因为分类不存在'.format(request.user.username))
			handle_illegal_access(request)
		if checkf(lambda: request.user.lawyer==category.lawyer): # [UnitTest]
			category.remove()
			messages.success(request, u'分类删除成功') 
			rec.success(u'{0} 删除分类 {1} 成功'.format(request.user.username,category.name))
			return response_auto(request, { 'success': True }, 'blogs:categories')
		else: # [UnitTest]
			handle_illegal_access(request, False)
			messages.error(request, u'分类删除失败')
			rec.error(u'{0} 删除分类 {1} 失败，因为权限不足'.format(request.user.username,category.name))
			return response_auto(request, { 'success': False }, 'blogs:categories')
	else: handle_illegal_access(request)

@login_required # [UnitTest]
def rename_category_view(request, pk_category):
	if request.method=='POST':
		rec=recorded(request,'blogs:rename_category')
		try:
			category=BlogCategory.objects.get(id=pk_category)
		except BlogCategory.DoesNotExist, e: # [UnitTest]
			rec.error(u'{0} 重命名分类失败，因为分类不存在'.format(request.user.username))
			handle_illegal_access(request)
		if checkf(lambda: request.user.lawyer==category.lawyer): # [UnitTest]
			category.name=request.POST['name']
			category.save()
			messages.success(request, u'分类重命名成功')
			rec.success(u'{0} 重命名分类 {1} 成功'.format(request.user.username,category.name))
			return response_auto(request, { 'success': True, 'pk':category.id, 'name':category.name  }, 'blogs:categories')
		else: # [UnitTest]
			handle_illegal_access(request, False)
			messages.error(request, u'分类重命名失败')
			rec.error(u'{0} 重命名分类 {1} 失败，因为权限不足'.format(request.user.username,category.name))
			return response_auto(request, { 'success': False }, 'blogs:categories')
	else: handle_illegal_access(request)
