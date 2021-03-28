from datetime import datetime

from django.shortcuts import resolve_url
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

	def test_str(self):
		self.assertEqual('Rodrigo Delfino', str(self.obj))

	def test_paid_default_to_false(self):
		""" By default paid must be false """
		self.assertEqual(False, self.obj.paid)

	def test_get_absolute_url(self):
		url = resolve_url('subscriptions:detail', self.obj.pk)
		self.assertEqual(url, self.obj.get_absolute_url())