from django.conf import settings
from django.core import mail
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def new(request):
	if request.method == 'POST':
		return create(request)

	return empty_form(request)


def empty_form(request):
	return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})


def create(request):
	form = SubscriptionForm(request.POST)

	if not form.is_valid():
		return render(request, 'subscriptions/subscription_form.html', {'form': form})

	subscription = form.save()

	_send_mail(
		subject='Confirmação de inscrição',
		from_email=settings.DEFAULT_FROM_EMAIL,
		to_email=[subscription.email],
		template_name='subscriptions/subscription_email.txt',
		context={'subscription': subscription}
	)
	return HttpResponseRedirect(resolve_url('subscriptions:detail', subscription.pk))


def detail(request, pk):
	try:
		subscription = Subscription.objects.get(pk=pk)
	except Subscription.DoesNotExist:
		raise  Http404
	except ValidationError:
		raise  Http404('Campo requisitado não é válido')

	return render(request, template_name='subscriptions/subscription_detail.html', context={'subscription': subscription})

def _send_mail(subject, from_email, to_email, template_name, context):
	body = render_to_string(template_name, context)

	mail.send_mail(subject=subject,
	               message=body,
	               from_email=from_email,
	               recipient_list=to_email)

