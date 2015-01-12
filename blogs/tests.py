# -*- coding: utf-8 -*-
from org.testingtools import *
from django.test import TestCase #, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class BasicTests(StaticLiveServerTestCase, TestingToolsMixin):
	fixtures = [
		'fixtures/accounts.json',
		'fixtures/blogs.json',
	]

	@classmethod
	def setUpClass(cls):
		cls.selenium = WebDriver()
		cls.selenium.maximize_window()
		super(BasicTests, cls).setUpClass()

	@classmethod
	def tearDownClass(cls):
		cls.selenium.quit()
		super(BasicTests, cls).tearDownClass()

	def test_home(self):
		self.login('lawyer0')
		self.nav("blogs:home")

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

"""
Public members of LiveServerTestCase:
['addCleanup', 'addTypeEqualityFunc', 'assertAlmostEqual', 'assertAlmostEquals', 
'assertContains', 'assertDictContainsSubset', 'assertDictEqual', 'assertEqual', 
'assertEquals', 'assertFalse', 'assertFieldOutput', 'assertFormError', 
'assertFormsetError', 'assertGreater', 'assertGreaterEqual', 'assertHTMLEqual', 
'assertHTMLNotEqual', 'assertIn', 'assertInHTML', 'assertIs', 'assertIsInstance', 
'assertIsNone', 'assertIsNot', 'assertIsNotNone', 'assertItemsEqual', 
'assertJSONEqual', 'assertLess', 'assertLessEqual', 'assertListEqual', 
'assertMultiLineEqual', 'assertNotAlmostEqual', 'assertNotAlmostEquals', 
'assertNotContains', 'assertNotEqual', 'assertNotEquals', 'assertNotIn', 
'assertNotIsInstance', 'assertNotRegexpMatches', 'assertNumQueries', 
'assertQuerysetEqual', 'assertRaises', 'assertRaisesMessage', 'assertRaisesRegexp', 
'assertRedirects', 'assertRegexpMatches', 'assertSequenceEqual', 'assertSetEqual', 
'assertTemplateNotUsed', 'assertTemplateUsed', 'assertTrue', 'assertTupleEqual', 
'assertXMLEqual', 'assertXMLNotEqual', 'assert_', 'available_apps', 'client', 
'client_class', 'countTestCases', 'debug', 'defaultTestResult', 'doCleanups', 
'fail', 'failIf', 'failIfAlmostEqual', 'failIfEqual', 'failUnless', 
'failUnlessAlmostEqual', 'failUnlessEqual', 'failUnlessRaises', 'failureException', 
'fixtures', 'id', 'live_server_url', 'longMessage', 'maxDiff', 'modify_settings', 
'reset_sequences', 'run', 'selenium', 'serialized_rollback', 'server_thread', 'setUp', 
'setUpClass', 'settings', 'shortDescription', 'skipTest', 'static_handler', 'tearDown', 
'tearDownClass', 'test_login']
"""

