from org.testingtools import *
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select

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
