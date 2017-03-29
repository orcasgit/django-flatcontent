from django.conf.urls import include, url
from django.contrib import admin

from .views import TemplateView


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^template-tag/$',
        TemplateView.as_view(template_name='template_tag.html'),
        name='template_tag'),
    url(r'^template-tag-as/$',
        TemplateView.as_view(template_name='template_tag_as.html'),
        name='template_tag_as'),
    url(r'^template-tag-with-site/$',
        TemplateView.as_view(template_name='template_tag_with_site.html'),
        name='template_tag_with_site'),
    url(r'^template-tag-with-extra-ctx/$',
        TemplateView.as_view(
            template_name='template_tag_with_extra_ctx.html',
            context={'ctx': 'Ctx'}
        ),
        name='template_tag_with_extra_ctx'),
    url(r'^template-tag-all-elements/$',
        TemplateView.as_view(template_name='template_tag_all_elements.html'),
        name='template_tag_all_elements'),
    url(r'^missing-as/$',
        TemplateView.as_view(template_name='missing_as.html'),
        name='missing_as'),
    url(r'^missing-with/$',
        TemplateView.as_view(template_name='missing_with.html'),
        name='missing_with'),
    url(r'^bad_arg_count/$',
        TemplateView.as_view(template_name='bad_arg_count.html'),
        name='bad_arg_count'),
    url(r'^bad_second_arg/$',
        TemplateView.as_view(template_name='bad_second_arg.html'),
        name='bad_second_arg')
]
