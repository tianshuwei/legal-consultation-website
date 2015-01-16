from org.testingtools import *

class FTest(FunctionalTestCase):
	fixtures = [
		'fixtures/accounts.json',
		'fixtures/blogs.json',
	]

	@classmethod
	def setUpClass(cls):
		cls.selenium = WebDriver()
		cls.selenium.maximize_window()
		super(FTest, cls).setUpClass()

	@classmethod
	def tearDownClass(cls):
		cls.selenium.quit()
		super(FTest, cls).tearDownClass()

	def test_new_article(self):
		self.login('lawyer0')
		self.nav("blogs:new_article")
		transacserial=self.transacserial_from('#frmArticle')
		self.find('#frmArticle [name="title"]').send_keys('New Article')
		Select(self.find('#frmArticle [name="category"]')).select_by_index(1)
		self.find('#frmArticle [name="tags"]').send_keys('test')
		self.find('#frmArticle [name="text"]').send_keys('New Article Text')
		self.find('#frmArticle [type="submit"]').click()
		time.sleep(1)
		self.assertTransaction(transacserial)

	def test_edit_article(self):
		self.login('lawyer0')
		self.nav("blogs:edit_article", pk_text=5)
		transacserial=self.transacserial_from('#frmArticle')
		self.find('#frmArticle [name="text"]').send_keys('Edit Test')
		self.find('#frmArticle [type="submit"]').click()
		time.sleep(1)
		self.assertTransaction(transacserial)

	def test_new_comment(self):
		self.login('lawyer0')
		self.nav("blogs:text", pk_text=5)
		transacserial=self.transacserial_from('#frmComment')
		self.find('#frmComment [name="txt_comment"]').send_keys('Nice')
		self.find('#frmComment [type="submit"]').click()
		time.sleep(1)
		self.assertTransaction(transacserial)

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
