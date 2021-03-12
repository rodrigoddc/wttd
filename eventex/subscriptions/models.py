import uuid

from django.db import models


class Subscription(models.Model):
	hash = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(verbose_name='nome', max_length=100)
	cpf = models.CharField(verbose_name='cpf', max_length=11)
	email = models.EmailField(verbose_name='e-mail')
	phone = models.CharField(verbose_name='telefone', max_length=20)
	created_at = models.DateTimeField(verbose_name='criado em', auto_now_add=True)

	class Meta:
		verbose_name_plural= 'inscrições'
		verbose_name = 'inscrição'
		ordering = ('-created_at', )

	def __str__(self):
		return self.name