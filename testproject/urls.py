from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    url(r'^template-tag/$',
        TemplateView.as_view(template_name='template_tag.html'),
        name='template_tag'),
    url(r'^template-tag-with-site/$',
        TemplateView.as_view(template_name='template_tag_with_site.html'),
        name='template_tag_with_site'),
    url(r'^bad_arg_count/$',
        TemplateView.as_view(template_name='bad_arg_count.html'),
        name='bad_arg_count'),
    url(r'^bad_second_arg/$',
        TemplateView.as_view(template_name='bad_second_arg.html'),
        name='bad_second_arg')
)
