from django.contrib import admin
from django.utils.timezone import now

from eventex.subscriptions.models import Subscription


class SubscriptionModelAdmin(admin.ModelAdmin):
	list_display = ('name', 'cpf', 'email', 'phone', 'created_at', 'subscribed_today', 'paid')
	list_filter = ('paid', 'created_at', )
	date_hierarchy = 'created_at'
	search_fields = ('name', 'email', 'phone', 'cpf')

	actions = ['mark_as_paid']

	def subscribed_today(self, obj):
		return obj.created_at.date() == now().date()

	subscribed_today.short_description = 'inscrito hoje?'
	subscribed_today.boolean = True

	def mark_as_paid(self, request, queryset):
		count = queryset.update(paid=True)

		if count == 1:
			message = f'{count} Inscrição foi marcada como paga.'
		else:
			message = f'{count} Inscrições foram marcadas como paga.'

		self.message_user(request, message)

	mark_as_paid.short_description = 'Marcar como pago'

admin.site.register(Subscription, SubscriptionModelAdmin)