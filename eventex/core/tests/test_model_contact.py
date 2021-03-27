from django.core.exceptions import ValidationError
from django.test import TestCase

from eventex.core.models import Speaker, Contact

class ContactModelTest(TestCase):
	def setUp(self) -> None:
		self.speaker = Speaker.objects.create(
			name='Rodrigo Delfino',
			slug='rodrigo-delfino',
			photo='http://hbn.link/hb-pic'
		)

	def test_email(self):
		contact = Contact.objects.create(
			speaker=self.speaker,
			kind=Contact.EMAIL,
			value='rodrigoddc1@gmail.com'
		)

		self.assertTrue(Contact.objects.exists())


	def test_phone(self):
		contact = Contact.objects.create(
			speaker=self.speaker,
			kind=Contact.PHONE,
			value='11-981097865'
		)

		self.assertTrue(Contact.objects.exists())

	def test_choices(self):
		""" Contacts kind should be limted to K or P """
		contact = Contact.objects.create(speaker=self.speaker, kind='A', value='B')

		self.assertRaises(ValidationError, contact.full_clean)

	def test_str(self):
		contact = Contact(speaker=self.speaker, kind=Contact.EMAIL, value='rodrigoddc1@gmail.com')
		self.assertEqual('rodrigoddc1@gmail.com', str(contact))


class ContactManagerTest(TestCase):
	def setUp(self) -> None:
		s = Speaker.objects.create(
								name='Rodrigo Delfino',
								slug='rodrigo-delfino',
								photo='https://images.fineartamerica.com/images-medium-large-5/sherlock-holmes-c1905-granger.jpg',
							)
		s.contact_set.create(kind=Contact.EMAIL, value='rodrigoddc1@gmail.com')
		s.contact_set.create(kind=Contact.PHONE, value='00-0000-0000')

	def test_emails(self):
		qs = Contact.objects.emails()
		expected = ['rodrigoddc1@gmail.com']
		self.assertQuerysetEqual(qs, expected, lambda obj: obj.value)

	def test_phones(self):
		qs = Contact.objects.phones()
		expected = ['00-0000-0000']
		self.assertQuerysetEqual(qs, expected, lambda obj: obj.value)
