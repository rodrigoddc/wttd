from django.shortcuts import resolve_url
from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
	def setUp(self) -> None:
		self.obj = Subscription.objects.create(
			name='Rodrigo Delfino',
			cpf='12345678900',
			email='a@a.com',
			phone='00-00000000'
		)
		self.response = self.client.get(resolve_url('subscriptions:detail', self.obj.hash))

	def test_get(self):
		self.assertEqual(200, self.response.status_code)


	def test_template(self):
		self.assertTemplateUsed(self.response, 'subscriptions/subscription_detail.html')

	def test_context(self):
		subscription = self.response.context['subscription']
		self.assertIsInstance(subscription, Subscription)

	def test_html(self):
		contents = (self.obj.name, self.obj.cpf, self.obj.email, self.obj.phone)

		with self.subTest():
			for expected in contents:
				self.assertContains(self.response, expected)


class SubscriptionDetailNotFound(TestCase):

	def test_not_found(self):
		import uuid
		response = self.client.get(resolve_url('subscriptions:detail', uuid.uuid4()))
		self.assertEqual(404, response.status_code)