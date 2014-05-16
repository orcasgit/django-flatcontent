"""
Tests in this file are for testing everything in flatcontent.admin
"""
import django

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase
from nose.tools import eq_

from flatcontent.models import FlatContent

from .basefactory import FlatContentFactory, UserFactory


class TestFlatContentAdmin(TestCase):
    """ Test all the flatcontent admin classes """

    def setUp(self):
        self.user = UserFactory.create()
        self.user.is_active = True
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.site = Site.objects.get()
        self.django_version = [int(v) for v in django.get_version().split('.')]

    def test_flatcontent_list(self):
        """ Test the list view for the FlatContent admin """
        self.client.login(username=self.user.username,
                          password='password')

        list_url = self._admin_url(FlatContent)
        add_url = self._admin_url(FlatContent, FlatContent())
        eq_(list_url, '/admin/flatcontent/flatcontent/')

        res = self.client.get(list_url)
        self.assertContains(res, '0 flat content')
        self.assertContains(res, add_url)

        flatcontent = FlatContentFactory(site=self.site)
        flatcontent.save()
        change_url = self._admin_url(FlatContent, flatcontent)
        res = self.client.get(list_url)
        self.assertContains(res, '1 flat content')
        self.assertRegexpMatches(res.content.decode(), '<tr.*%s.*%s.*%s.*</tr>' % (
          flatcontent.slug, flatcontent.site, flatcontent.content
        ))
        if self.django_version[0] >= 1 and self.django_version[1] > 4:
            self.assertContains(res, change_url)
        else:
            # Django 1.4 used relative change url
            self.assertContains(res, '%i/' % flatcontent.id)
        self.assertContains(res, add_url)

    def _admin_url(self, model, obj=None):
        """ Utility method to get an admin url for a model """
        content_type = ContentType.objects.get_for_model(model)
        uri = "admin:%s_%s" % (content_type.app_label, content_type.model)
        args = ()
        if obj and not obj.id:
            uri += '_add'
        elif obj:
            uri += '_change'
            args = (obj.id,)
        else:
            uri += '_changelist'
        return reverse(uri, args=args)
