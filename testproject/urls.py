from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns(
    '',
    url(r'^show-flatcontent/$',
        TemplateView.as_view(template_name='content.html'),
        name='show_flatcontent')
)
