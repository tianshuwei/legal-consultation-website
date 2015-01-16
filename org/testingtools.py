# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from index.models import TransactionRecord
from org.tools import transacserial, TRANSACSERIAL
import traceback, time

class FTestingToolsMixin(object):
	def reverse(self, url_ref, **kwargs):
		return self.live_server_url+reverse(url_ref, kwargs=kwargs)

	def nav(self, url_ref, **kwargs):
		self.selenium.get(self.reverse(url_ref,**kwargs))

	def login(self, username, password='1234'):
		self.selenium.get(self.reverse("accounts:login"))
		username_input = self.selenium.find_element_by_name("username")
		username_input.send_keys(username)
		password_input = self.selenium.find_element_by_name("password")
		password_input.send_keys(password)
		self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

	def find(self, selector):
		elem=self.selenium.find_element_by_css_selector(selector)
		elem.find=elem.find_element_by_css_selector
		return elem

	def transacserial_from(self, selector):
		return self.find(selector).find('input[name="transacserial"]').get_attribute('value')

	def query_transaction(self, serial):
		try: 
			rec=TransactionRecord.objects.get(serial=serial)
			return rec.result=='success'
		except TransactionRecord.DoesNotExist, e: 
			return False

	def assertTransaction(self, serial):
		self.assertTrue(self.query_transaction(serial))

class UTestingToolsMixin(object):
	def reverse(self, url_ref, **kwargs):
		return reverse(url_ref, kwargs=kwargs)

	def nav(self, url_ref, **kwargs):
		self.client.get(self.reverse(url_ref,**kwargs))

	def login(self, username, password='1234'):
		self.client.post(self.reverse("accounts:login"), {
			'username': username,
			'password': password,
			TRANSACSERIAL: transacserial('login'),
		})

	def post(self, data, url_ref, **kwargs):
		data[TRANSACSERIAL]=transacserial(url_ref)
		self.client.post(self.reverse(url_ref, **kwargs), data)
		return data[TRANSACSERIAL]

	def transacserial(self, transaction_name):
		return transacserial(transaction_name)

	def query_transaction(self, serial):
		try: 
			rec=TransactionRecord.objects.get(serial=serial)
			return rec.result=='success'
		except TransactionRecord.DoesNotExist, e: 
			return False

	def assertTransaction(self, serial):
		self.assertTrue(self.query_transaction(serial))

from django.test import TestCase #, LiveServerTestCase
from django.test.client import Client
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.select import Select
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTestCase(StaticLiveServerTestCase, FTestingToolsMixin):
	"""
	功能测试基类，多重继承测试工具
	"""

class UnitTestCase(TestCase, UTestingToolsMixin):
	"""
	单元测试基类，多重继承测试工具
	"""

"""
Assertion methods:
['assertAlmostEqual', 'assertAlmostEquals', 
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
'assertXMLEqual', 'assertXMLNotEqual']
"""
