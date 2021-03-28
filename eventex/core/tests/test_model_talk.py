from django.test import  TestCase

from eventex.core.models import Talk, Course
from eventex.core.templates.core.managers import PeriodManager


class TalkModelTest(TestCase):
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

	def test_ordering(self):
		self.assertListEqual(['start'], Talk._meta.ordering)

class PeriodManagerTest(TestCase):
	def setUp(self) -> None:
		Talk.objects.create(title='Morning Talk', start='11:59')
		Talk.objects.create(title='Afternoon Talk', start='12:00')

	def test_manager(self):
		self.assertIsInstance(Talk.objects, PeriodManager)

	def test_at_morning(self):
		qs = Talk.objects.at_morning()
		expected = ['Morning Talk']
		self.assertQuerysetEqual(qs, expected, lambda o: o.title)

	def test_at_afternoon(self):
		qs = Talk.objects.at_afternoon()
		expected = ['Afternoon Talk']
		self.assertQuerysetEqual(qs, expected, lambda o: o.title)


class CourseModelTest(TestCase):
	def setUp(self) -> None:
		self.course = Course.objects.create(title='Título do curso', start='09:00', description='Descrição do curso',
		                                       slots=20)

	def test_create(self):
		self.assertTrue(Course.objects.exists())

	def test_speakers(self):
		""" Course has many spealers and vice-versa """
		self.course.speakers.create(name='Rodrigo Delfino', slug='rodrigo-delfino',
		                            website='google.com/rodrigo.webp')

		self.assertEqual(1, self.course.speakers.count())

	def test_str(self):
		self.assertEqual('Título do curso', str(self.course))

	def test_manager(self):
		self.assertIsInstance(Course.objects, PeriodManager)

	def test_ordering(self):
		self.assertListEqual(['start'], Course._meta.ordering)