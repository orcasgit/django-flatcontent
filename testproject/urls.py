from django.conf.urls import patterns, url
from django.views.generic import TemplateView


urlpatterns = patterns(
    '',
    url(r'^template-tag/$',
        TemplateView.as_view(template_name='template_tag.html'),
        name='template_tag'),
    url(r'^bad_arg_count/$',
        TemplateView.as_view(template_name='bad_arg_count.html'),
        name='bad_arg_count')
)
