from django.shortcuts import resolve_url
from django.test import TestCase

from eventex.core.models import Talk, Speaker


class TalkListGet(TestCase):
	def setUp(self) -> None:
		talk_1 = Talk.objects.create(title='Título da palestra',
		                             start='10:00',
		                             description='Descrição da palestra')
		talk_2 = Talk.objects.create(title='Título da palestra',
		                             start='13:00',
		                             description='Descrição da palestra')
		course_1 = Talk.objects.create(title='Título do Curso',
		                               start='09:00',
		                               description='Descrição do Curso')

		speaker = Speaker.objects.create(
			name='Alan Turing',
			slug='alan-turing',
			website='http://alanturing.net/'
		)

		talk_1.speakers.add(speaker)
		talk_2.speakers.add(speaker)
		course_1.speakers.add(speaker)

		self.response = self.client.get(resolve_url('talk_list'))


	def test_get(self):
		self.assertEqual(200, self.response.status_code)

	def test_template(self):
		self.assertTemplateUsed(self.response, 'core/talk_list.html')

	def test_html(self):
		contents = [
			(2, 'Título da palestra'),
			(1, '10:00'),
			(1, '13:00'),
			(3, '/palestrantes/alan-turing/'),
			(3, 'Alan Turing'),
			(2, 'Descrição da palestra'),
			(1, 'Título do Curso'),
			(1, '09:00'),
			(1, 'Descrição do Curso'),
		]
		for count, expected in contents:
			with self.subTest():
				self.assertContains(self.response,  count=count, text=expected)

	def test_context(self):
		variables = ['morning_talks', 'afternoon_talks']
		for key in variables:
			with self.subTest():
				self.assertIn(key, self.response.context)


class TalkListGetEmpty(TestCase):
	def test_get_empty(self):
		response = self.client.get(resolve_url('talk_list'))
		context = ['Ainda não existem palestras no período manhã',
		            'Ainda não existem palestras no período tarde']

		for expected in context:
			with self.subTest():
				self.assertContains(response=response, text=expected)
