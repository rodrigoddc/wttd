from unittest.mock import Mock

from django.test import TestCase
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin

class SubscriptionModelAdminTest(TestCase):

	def setUp(self) -> None:
		Subscription.objects.create(
			name='Rodrigo Delfino',
			cpf='1234657900',
			email='a@a.com',
			phone='00-00000000'
		)
		self.model_admin = SubscriptionModelAdmin(model=Subscription, admin_site=admin.site)

	def test_has_action(self):
		"""Action marked as paid should be instaled """
		self.assertIn('mark_as_paid', self.model_admin.actions)

	def test_mark_all(self):
		""" Should mark all selections subscriptions as paid """
		self.call_action()
		self.assertEqual(1, Subscription.objects.filter(paid=True).count())

	def test_message(self):
		""" Should send a message to the user """
		mock = self.call_action()
		mock.assert_called_once_with(None, '1 Inscrição foi marcada como paga.')


	def call_action(self):
		queryset = Subscription.objects.all()

		mock = Mock()
		old_message_user = SubscriptionModelAdmin.message_user
		SubscriptionModelAdmin.message_user = mock

		self.model_admin.mark_as_paid(None, queryset)

		SubscriptionModelAdmin.message_user = old_message_user

		return mock
