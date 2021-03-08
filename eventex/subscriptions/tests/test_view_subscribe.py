from django.core import mail
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


class SubscribePostTest(TestCase):
	def setUp(self):
		data = dict(name="Rodrigo Delfino", cpf="12345678900", email="a@a.com", phone="00-0000-0000")
		self.response = self.client.post('/inscricao/', data)

	def test_post(self):
		""" Valid POST should redirect to /inscricao/ """
		self.assertEqual(302, self.response.status_code)

	def test_send_subscribe_email(self):
		self.assertEqual(1, len(mail.outbox))

	def test_subscription_email_subject(self):
		email = mail.outbox[0]
		expect = 'Confirmação de inscrição'

		self.assertEqual(expect, email.subject)

	def test_subscription_email_from(self):
		email = mail.outbox[0]
		expect = 'rodrigoddc1@gmail.com'

		self.assertEqual(expect, email.from_email)

	def test_subscription_email_to(self):
		email = mail.outbox[0]
		expect = ['rodrigoddc1@gmail.com', 'a@a.com']

		self.assertEqual(expect, email.recipients())

	def test_subscription_email_message(self):
		email = mail.outbox[0]

		self.assertIn('Rodrigo Delfino', email.body)
		self.assertIn('12345678900', email.body)
		self.assertIn('a@a.com', email.body)
		self.assertIn('00-0000-0000', email.body)


class InvalidSubscribePost(TestCase):
	def setUp(self) -> None:
		self.response = self.client.post('/inscricao/', {})

	def test_post(self):
		""" Invalid POST should not be redirect """
		self.assertEqual(200, self.response.status_code)

	def test_template(self):
		""" ON ERROR must return to /inscricao/ using subscription_form.html """
		self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

	def test_has_form(self):
		""" ON ERROR must return right form """
		form = self.response.context['form']
		self.assertIsInstance(form, SubscriptionForm)

	def test_form_has_errors(self):
		""" ON ERROR must return form with erros """
		form = self.response.context['form']
		self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):

	def test_message(self):
		data = dict(
			name='Rodrigo Delfino',
			cpf='12345678900',
			email='a@a.com',
			phone='00-0000-0000'
		)

		response = self.client.post('/inscricao/', data, follow=True)
		self.assertContains(response, 'Inscrição realizada com sucesso!')