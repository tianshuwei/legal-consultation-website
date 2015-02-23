from org.testingtools import *

class AuthTest(UnitTestCase):
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

class QuestionTest(UnitTestCase):
	fixtures = [
		'fixtures/accounts.json',
	]

	def test_new_question(self):
		self.login('client0')
		self.assertTrue(self.post({
			'title':'New Question',
			'lawyer':'3',
			'description':'New Question Content',
		},'accounts:new_question'))

	def test_new_question_by_lawyer_attempt(self):
		self.login('lawyer0')
		self.assertFalse(self.post({
			'title':'New Question',
			'lawyer':'3',
			'description':'New Question Content',
		},'accounts:new_question'))
