# -*- coding: utf-8 -*-
from org.testingtools import *
from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class BasicTests(LiveServerTestCase, TestingToolsMixin):
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

	def test_00login(self):
		self.login('lawyer0')
		self.selenium.get(self.reverse("index:index"))

	def test_01home(self):
		self.login('lawyer0')
		self.selenium.get(self.reverse("blogs:home"))

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

