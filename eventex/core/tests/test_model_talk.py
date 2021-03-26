from django.test import  TestCase

from eventex.core.models import Talk

class TalkModel(TestCase):
	def setUp(self) -> None:
		self.talk = Talk.objects.create(
			title='Título da palestra',
		)

	def test_create(self):
		self.assertTrue(Talk.objects.exists())

	def test_has_speakers(self):
		""" Talk has many Spealers and vice-versa """
		self.talk.speakers.create(
			name='Alan Turing',
			slug='alan-turing',
			website='http://alanturing.net/'
		)
		self.assertEqual(1, self.talk.speakers.count())

	def test_description_blank(self):
		""" Field description must be able to be blank """
		field = Talk._meta.get_field('description')
		self.assertTrue(field.blank)

	def test_speakers_blank(self):
		""" Field speakers could be blank """
		field = Talk._meta.get_field('speakers')
		self.assertTrue(field.blank)

	def test_start_blank(self):
		""" Field start could be blank """
		field = Talk._meta.get_field('start')
		self.assertTrue(field.blank)

	def test_start_null(self):
		""" Field start could be null """
		field = Talk._meta.get_field('start')
		self.assertTrue(field.null)

	def test_str(self):
		self.assertEqual('Título da palestra', self.talk.title)