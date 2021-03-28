import uuid

from django.db import models
from django.shortcuts import resolve_url

from eventex.subscriptions.validators import validate_cpf


class Subscription(models.Model):
	hash = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(verbose_name='nome', max_length=100)
	cpf = models.CharField(verbose_name='cpf', max_length=11, validators=[validate_cpf])
	email = models.EmailField(verbose_name='e-mail', blank=True)
	phone = models.CharField(verbose_name='telefone', max_length=20, blank=True)
	created_at = models.DateTimeField(verbose_name='criado em', auto_now_add=True)
	paid = models.BooleanField(verbose_name='pago', default=False)

	class Meta:
		verbose_name_plural= 'inscrições'
		verbose_name = 'inscrição'
		ordering = ('-created_at', )

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return resolve_url('subscriptions:detail', self.pk)