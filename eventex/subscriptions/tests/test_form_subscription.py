from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):

	def test_form_has_fields(self):
		""" FORM must have 4 fields """
		form = SubscriptionForm()
		expected = ['name', 'cpf', 'email', 'phone']
		self.assertSequenceEqual(expected, list(form.fields))

	def test_cpf_is_digit(self):
		"""	Cpf field must only accept digits """
		form = self.make_validated_form(cpf='abcd5678900')
		self.assertFormErrorCode(form, field='cpf', code='digits')

	def test_cpf_has_11_digits(self):
		""" CPF field must have 11 digits """
		form = self.make_validated_form(cpf='1234')
		self.assertFormErrorCode(form=form, field='cpf', code='length')

	def test_name_must_be_capitalized(self):
		""" NAME field must be capitalized """
		form = self.make_validated_form(name='RODRIGO delfino')
		self.assertEqual('Rodrigo Delfino', form.cleaned_data['name'])

	def test_email_is_optional(self):
		""" EMAIL field must be optional """
		form = self.make_validated_form(email='')
		self.assertFalse(form.errors)

	def test_phone_is_optional(self):
		""" PHONE field must be optional """
		form = self.make_validated_form(phone='')
		self.assertFalse(form.errors)

	def test_must_informe_email_or_phone(self):
		""" EMAIL and PHONE are optional, but one must ve informed """
		form = self.make_validated_form(email='', phone='')
		self.assertListEqual(['__all__'], list(form.errors))

	def assertFormErrorCode(self, form, field, code):
		""" AUX assert method to build form with respectives validation code errors to compare """
		errors = form.errors.as_data()
		errors_list = errors[field]
		exception = errors_list[0]
		self.assertEqual(code, exception.code)

	def assertFormErrorMessage(self, form, field, message):
		""" AUX assert method to make a form with necessary validation error messages to compare """
		errors = form.errors
		errors_list = errors[field]
		self.assertListEqual([message], errors_list)

	def make_validated_form(self, **kwargs):
		valid = dict(name='Rodrigo Delfino',
		            email='a@a.com',
		            phone='00-00000000',
		            cpf='12345678900')
		data = dict(valid, **kwargs)

		form = SubscriptionForm(data)
		form.is_valid()
		return form