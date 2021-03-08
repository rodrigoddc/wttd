from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
	if request.method == 'POST':
		return create(request)
	else:
		return new(request)

def create(request):
	form = SubscriptionForm(request.POST)

	if not form.is_valid():
		return render(request, 'subscriptions/subscription_form.html', {'form': form})

	_send_mail(
		subject='Confirmação de inscrição',
		from_email=settings.DEFAULT_FROM_EMAIL,
		to_email=[form.cleaned_data['email']],
		template_name='subscriptions/subscription_email.txt',
		context=form.cleaned_data
	)
	Subscription.objects.create(**form.cleaned_data)

	messages.success(request, 'Inscrição realizada com sucesso!')

	return HttpResponseRedirect('/inscricao/')

def new(request):
	return render(request, 'subscriptions/subscription_form.html', {'form': SubscriptionForm()})

def _send_mail(subject, from_email, to_email, template_name, context):
	body = render_to_string(template_name, context)

	mail.send_mail(subject=subject,
	               message=body,
	               from_email=from_email,
	               recipient_list=to_email)


