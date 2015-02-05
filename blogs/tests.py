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

	def test_delete_category_not_exist_attempt(self):
		self.login('lawyer0')
		self.assertFalse(self.post({
		},'blogs:delete_category', pk_category=100))

	def test_delete_category_unauthorized_attempt(self):
		self.login('client0')
		self.assertFalse(self.post({
		},'blogs:delete_category', pk_category=1))

	def test_rename_category(self):
		self.login('lawyer0')
		self.assertTrue(self.post({
			'name':'new name',
		},'blogs:rename_category', pk_category=1))

	def test_rename_category_not_exist_attempt(self):
		self.login('lawyer0')
		self.assertFalse(self.post({
			'name':'new name',
		},'blogs:rename_category', pk_category=100))

	def test_rename_category_unauthorized_attempt(self):
		self.login('client0')
		self.assertFalse(self.post({
			'name':'new name',
		},'blogs:rename_category', pk_category=1))

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

	def test_new_comment_on_article_not_exist(self):
		self.login('lawyer0')
		self.assertFalse(self.post({
			'txt_comment':'Nice',
		},'blogs:new_comment',pk_text=500))
