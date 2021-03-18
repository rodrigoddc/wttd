from django.test import TestCase
from django.shortcuts import resolve_url


class HomeTest(TestCase):
	fixtures = ['keynotes.json']
	def setUp(self):
		self.response = self.client.get(resolve_url('home'))

	def test_get(self):
		"""
		GET / must return status code 200
		"""
		self.assertEqual(200, self.response.status_code)

	def test_template(self):
		"""GET / must use index.html """
		self.assertTemplateUsed(self.response, 'index.html')

	def test_subscription_link(self):
		""" GET / must contain subscription link """
		expected = f"""href="{resolve_url('subscriptions:new')}"""
		self.assertContains(self.response, expected)

	def test_speakers(self):
		""" GET / must show keynotes speakers """
		contents = [
			f'href="{resolve_url("speaker_detail", slug="grace-hopper")}"',
			'Grace Hopper',
			'http://hbn.link/hopper-pic',
			f'href="{resolve_url("speaker_detail", slug="alan-turing")}"',
			'Alan Turing',
			'http://hbn.link/turing-pic'
		]
		for expected in contents:
			with self.subTest():
				self.assertContains(self.response, expected)

	def test_nav_links(self):
		contents =[
			f'href="{resolve_url("home")}#overview"',
			f'href="{resolve_url("home")}#speakers"',
			f'href="{resolve_url("home")}#sponsors"',
			f'href="{resolve_url("home")}#register"',
			f'href="{resolve_url("home")}#venue"',
		]
		for expected in contents:
			with self.subTest():
				self.assertContains(self.response, expected)