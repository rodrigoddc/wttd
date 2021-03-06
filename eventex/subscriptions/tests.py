from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
	def setUp(self):
		self.response = self.client.get('/inscricao/')

	def test_get(self):
		""" Must return status code 200 """
		self.assertEqual(200, self.response.status_code)

	def test_template(self):
		""" Must use template subscriptions/subscription_form.html """
		self.assertTemplateUsed(self.response, template_name='subscriptions/subscription_form.html')

	def test_html(self):
		""" Must contain html tags"""
		self.assertContains(self.response, text='<form')
		self.assertContains(self.response, text='<input', count=6)
		self.assertContains(self.response, text='type="text"', count=3)
		self.assertContains(self.response, text='type="email"')
		self.assertContains(self.response, text='type="submit"')

	def test_csrf(self):
		""" HTML must contains csrf """
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_has_form(self):
		""" CONTEXT must have subscription form """
		form = self.response.context['form']
		self.assertIsInstance(form, SubscriptionForm)

	def test_form_has_fields(self):
		""" FORM must have 4 fields """
		form = self.response.context['form']
		self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))
