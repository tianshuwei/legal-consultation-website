from org.testingtools import *

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
		},'questions:new_question'))

	def test_new_question_by_lawyer_attempt(self):
		self.login('lawyer0')
		self.assertFalse(self.post({
			'title':'New Question',
			'lawyer':'3',
			'description':'New Question Content',
		},'questions:new_question'))
