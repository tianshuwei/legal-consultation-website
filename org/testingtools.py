# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from index.models import TransactionRecord
import traceback, time

class TestingToolsMixin(object):
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
