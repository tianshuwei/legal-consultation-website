from org.testingtools import *
# from blogs.optional_tests import FTest

class CategoryTest(UnitTestCase):
	fixtures = [
		'fixtures/accounts.json',
		'fixtures/blogs.json',
	]

	def setUp(self):
		self.client = Client()

	def test_new_category(self):
		self.login('lawyer0')
		self.assertTrue(self.post({
			'name':'new category',
		},'blogs:categories'))
		
	def test_new_category_attempt_by_client(self):
		self.login('client0')
		self.assertFalse(self.post({
			'name':'new category',
		},'blogs:categories'))

	def test_new_dup_category_attempt(self):
		self.login('lawyer0')
		self.assertTrue(self.post({
			'name':'new category dup',
		},'blogs:categories'))
		self.assertFalse(self.post({
			'name':'new category dup',
		},'blogs:categories'))

	def test_delete_category(self):
		self.login('lawyer0')
		self.assertTrue(self.post({
		},'blogs:delete_category', pk_category=1))

	def test_delete_category_that_doesnt_exist_attempt(self):
		self.login('lawyer0')
		self.assertFalse(self.post({
		},'blogs:delete_category', pk_category=100))

	def test_delete_category_unauthorized_attempt(self):
		self.login('lawyer1')
		self.assertFalse(self.post({
		},'blogs:delete_category', pk_category=1))

	def test_delete_category_unauthorized_attempt2(self):
		self.login('client0')
		self.assertFalse(self.post({
		},'blogs:delete_category', pk_category=1))

	def test_rename_category(self):
		self.login('lawyer0')
		self.assertTrue(self.post({
			'name':'new name',
		},'blogs:rename_category', pk_category=1))

	def test_rename_category_that_doesnt_exist_attempt(self):
		self.login('lawyer0')
		self.assertFalse(self.post({
			'name':'new name',
		},'blogs:rename_category', pk_category=100))

	def test_rename_category_unauthorized_attempt(self):
		self.login('lawyer1')
		self.assertFalse(self.post({
			'name':'new name',
		},'blogs:rename_category', pk_category=1))

	def test_delete_category_unauthorized_attempt2(self):
		self.login('client0')
		self.assertFalse(self.post({
		},'blogs:delete_category', pk_category=1))

class CommentTest(UnitTestCase):
	fixtures = [
		'fixtures/accounts.json',
		'fixtures/blogs.json',
	]

	def setUp(self):
		self.client = Client()

	def test_new_comment(self):
		self.login('lawyer0')
		self.assertTrue(self.post({
			'txt_comment':'Nice',
		},'blogs:new_comment',pk_text=5))

	def test_new_comment_by_client(self):
		self.login('client0')
		self.assertTrue(self.post({
			'txt_comment':'Nice',
		},'blogs:new_comment',pk_text=5))

	def test_new_comment_on_article_that_doesnt_exist_attempt(self):
		self.login('lawyer0')
		self.assertFalse(self.post({
			'txt_comment':'Nice',
		},'blogs:new_comment',pk_text=500))

class ArticleTest(UnitTestCase):
	fixtures = [
		'fixtures/accounts.json',
		'fixtures/blogs.json',
	]

	sample_text="""Lorem ipsum dolor sit amet, consectetur adipisicing elit. 
	Atomus, appellat dedocendi omnes quoddam atomos."""

	def setUp(self):
		self.client = Client()

	def test_new_article(self):
		self.login('lawyer0')
		self.assertTrue(self.post({
			'title': 'New Article',
			'category': 1,
			'tags': 'test',
			'text': ArticleTest.sample_text
		},'blogs:new_article'))

	def test_new_article_by_client_attempt(self):
		self.login('client0')
		self.assertFalse(self.post({
			'title': 'New Article',
			'category': 1,
			'tags': 'test',
			'text': ArticleTest.sample_text
		},'blogs:new_article'))

	def test_new_article_in_category_that_doesnt_exist_attempt(self):
		self.login('lawyer0')
		self.assertFalse(self.post({
			'title': 'New Article',
			'category': 100,
			'tags': 'test',
			'text': ArticleTest.sample_text
		},'blogs:new_article'))

	def test_edit_article(self):
		self.login('lawyer0')
		self.assertTrue(self.post({
			'title': 'Edit Article',
			'category': 1,
			'tags': 'test',
			'text': ArticleTest.sample_text
		},'blogs:edit_article', pk_text=5))

	def test_edit_article_unauthorized_attempt(self):
		self.login('lawyer1')
		self.assertFalse(self.post({
			'title': 'Edit Article',
			'category': 1,
			'tags': 'test',
			'text': ArticleTest.sample_text
		},'blogs:edit_article', pk_text=5))

	def test_edit_article_unauthorized_attempt2(self):
		self.login('client1')
		self.assertFalse(self.post({
			'title': 'Edit Article',
			'category': 1,
			'tags': 'test',
			'text': ArticleTest.sample_text
		},'blogs:edit_article', pk_text=5))

	def test_delete_article(self):
		self.login('lawyer0')
		self.assertTrue(self.post({
			'title': 'Edit Article',
			'category': 1,
			'tags': 'test',
			'text': ArticleTest.sample_text
		},'blogs:edit_article', pk_text=5))

	def test_delete_article_unauthorized_attempt(self):
		self.login('lawyer1')
		self.assertFalse(self.post({
			'title': 'Edit Article',
			'category': 1,
			'tags': 'test',
			'text': ArticleTest.sample_text
		},'blogs:edit_article', pk_text=5))

	def test_delete_article_unauthorized_attempt2(self):
		self.login('client1')
		self.assertFalse(self.post({
			'title': 'Edit Article',
			'category': 1,
			'tags': 'test',
			'text': ArticleTest.sample_text
		},'blogs:edit_article', pk_text=5))

