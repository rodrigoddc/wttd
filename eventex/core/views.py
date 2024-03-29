from django.views.generic import DetailView
from django.views.generic.list import ListView

from eventex.core.models import Speaker, Talk

# class HomeView(ListView):
# 	template_name = 'index.html'
# 	model = Speaker
#
home = ListView.as_view(template_name='index.html', model=Speaker)

speaker_detail = DetailView.as_view(model=Speaker)

talk_list = ListView.as_view(template_name='core/talk_list.html', model=Talk)