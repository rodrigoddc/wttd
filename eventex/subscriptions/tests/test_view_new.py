from django.test import TestCase
from django.shortcuts import resolve_url
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
	def setUp(self):
		self.response = self.client.get(resolve_url('subscriptions:new'))

	def test_get(self):
		""" Must return status code 200 """
		self.assertEqual(200, self.response.status_code)

	def test_template(self):
		""" Must use template subscriptions/subscription_form.html """
		self.assertTemplateUsed(self.response, template_name='subscriptions/subscription_form.html')

	def test_html(self):
		""" Must contain html tags"""
		tags = (
			('<form', 1),
			('<input', 6),
			('type="text"', 3),
			('type="email"', 1),
			('type="submit"', 1),
		)
		for text, count in tags:
			with self.subTest():
				self.assertContains(self.response, text, count)

	def test_csrf(self):
		""" HTML must contains csrf """
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_has_form(self):
		""" CONTEXT must have subscription form """
		form = self.response.context['form']
		self.assertIsInstance(form, SubscriptionForm)


class SubscriptionsNewPostValid(TestCase):
	def setUp(self):
		self.data = dict(name="Rodrigo Delfino", cpf="12345678900",
		            email="a@a.com", phone="00-0000-0000")
		self.response = self.client.post(resolve_url('subscriptions:new'), self.data)

	def test_post(self):
		""" Valid POST should redirect to /inscricao/hash/ """
		obj = Subscription.objects.first()
		self.assertRedirects(self.response, resolve_url('subscriptions:detail', obj.hash))

	def test_save_sibscription(self):
		self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):
	def setUp(self) -> None:
		self.response = self.client.post(resolve_url('subscriptions:new'), {})

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

	def test_dont_save_subscription(self):
		self.assertFalse(Subscription.objects.exists())


class TemplateRegretionTest(TestCase):
	def test_template_has_non_field_errors(self):
		invalid_data = dict(name='Rodrigo Delfino', cpf='12345678900')
		response = self.client.post(resolve_url('subscriptions:new'), invalid_data)

		self.assertContains(response, '<ul class="errorlist nonfield">')