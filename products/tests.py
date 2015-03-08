from org.testingtools import *

class OrderTest(UnitTestCase):
	fixtures = [
		'fixtures/accounts.json',
		'fixtures/products.json',
	]

	def setUp(self):
		self.client = Client()
