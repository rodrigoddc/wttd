from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):
	def setUp(self) -> None:
		self.obj = Subscription(
			name='Rodrigo Delfino',
			cpf='12345678900',
			email='rodrigoddc1@gmail.com',
			phone='00-00000000'
		)
		self.obj.save()

	def test_create(self):
		self.assertTrue(Subscription.objects.exists())

	def test_created_at(self):
		""" Subscriptions must have an auto created_at attribute"""
		self.assertIsInstance(self.obj.created_at, datetime)