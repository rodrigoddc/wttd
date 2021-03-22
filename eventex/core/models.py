from django.db import models

# Create your models here.
from django.shortcuts import resolve_url


class Speaker(models.Model):
	name = models.CharField('nome', max_length=255)
	slug = models.SlugField('slug')
	photo = models.URLField('foto')
	website = models.URLField('website', blank=True)
	description = models.TextField('descrição', blank=True)

	class Meta:
		verbose_name = 'palestrante'
		verbose_name_plural = 'palestrantes'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return resolve_url('speaker_detail', slug=self.slug)


class Contact(models.Model):
	EMAIL = 'E'
	PHONE = 'P'

	KINDS = (
		(EMAIL, 'Email'),
		(PHONE, 'Telefone')
	)

	speaker = models.ForeignKey('Speaker', verbose_name='palestrante', on_delete=models.CASCADE)
	kind = models.CharField(verbose_name='tipo', max_length=1, choices=KINDS)
	value = models.CharField(verbose_name='valor', max_length=255)

	class Meta:
		verbose_name = 'contato'
		verbose_name_plural = 'contatos'

	def __str__(self):
		return self.value