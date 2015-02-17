from org.testingtools import *

class CategoryTest(UnitTestCase):
	fixtures = [
		'fixtures/accounts.json',
	]

	def setUp(self):
		self.client = Client()

	def test_login_by_lawyer(self):
		self.assertTrue(self.post({
			'username':'lawyer0',
			'password':'1234'
		},'accounts:login'))

	def test_login_by_client(self):
		self.assertTrue(self.post({
			'username':'client0',
			'password':'1234'
		},'accounts:login'))

	def test_login_random_attempt(self):
		self.assertFalse(self.post({
			'username':'user_that_doesnt_exist',
			'password':'just_a_guess'
		},'accounts:login'))

	def test_register_lawyer(self):
		self.assertTrue(self.post({
			'username':'lawyer100',
			'password':'1234',
			'email':'test@example.com',
			'last_name':'Doe',
			'first_name':'John',
		},'accounts:register', role='lawyer'))

	def test_register_client(self):
		self.assertTrue(self.post({
			'username':'client100',
			'password':'1234',
			'email':'test@example.com',
			'last_name':'Doe',
			'first_name':'John',
		},'accounts:register', role='client'))

	def test_new_question(self):
		pass
