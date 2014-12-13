# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
import traceback

class TestingToolsMixin(object):
	def reverse(self, url_ref, **kwargs):
		return self.live_server_url+reverse(url_ref, kwargs=kwargs)

	def login(self, username, password='1234'):
		self.selenium.get(self.reverse("accounts:login"))
		username_input = self.selenium.find_element_by_name("username")
		username_input.send_keys(username)
		password_input = self.selenium.find_element_by_name("password")
		password_input.send_keys(password)
		self.selenium.find_element_by_xpath('//button[@type="submit"]').click()

