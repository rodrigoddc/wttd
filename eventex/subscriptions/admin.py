from django.contrib import admin
from django.utils.timezone import now

from eventex.subscriptions.models import Subscription


class SubscriptionModelAdmin(admin.ModelAdmin):
	list_display = ('name', 'cpf', 'email', 'phone', 'created_at', 'subscribed_today')
	list_filter = ('created_at', )
	date_hierarchy = 'created_at'
	search_fields = ('name', 'email', 'phone', 'cpf')

	def subscribed_today(self, obj):
		return obj.created_at.date() == now().date()

	subscribed_today.short_description = 'inscrito hoje?'
	subscribed_today.boolean = True

admin.site.register(Subscription, SubscriptionModelAdmin)