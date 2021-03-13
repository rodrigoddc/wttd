from django.core import mail
from django.shortcuts import resolve_url
from django.test import TestCase


class SubscribePostValid(TestCase):
	def setUp(self):
		data = dict(name="Rodrigo Delfino", cpf="12345678900", email="a@a.com", phone="00-0000-0000")
		self.client.post(resolve_url('subscriptions:new'), data)
		self.email = mail.outbox[0]

	def test_send_subscribe_email(self):
		self.assertEqual(1, len(mail.outbox))

	def test_subscription_email_subject(self):
		expect = 'Confirmação de inscrição'

		self.assertEqual(expect, self.email.subject)

	def test_subscription_email_from(self):
		expect = 'rodrigoddc1@gmail.com'
		self.assertEqual(expect, self.email.from_email)

	def test_subscription_email_to(self):
		expect = ['a@a.com']
		self.assertEqual(expect, self.email.to)

	def test_subscription_email_message(self):

		contents = [
			'Rodrigo Delfino',
			'12345678900',
			'a@a.com',
			'00-0000-0000'
		]
		for content in contents:
			with self.subTest():
				self.assertIn(content, self.email.body)
