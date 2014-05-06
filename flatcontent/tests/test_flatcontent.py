from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template import TemplateSyntaxError
from django.test import TestCase
from nose.tools import eq_

from flatcontent.models import FlatContent
from .basefactory import FlatContentFactory, SiteFactory


class TestFlatContent(TestCase):

    def setUp(self):
        self.site = Site.objects.get()
        self.flat_content = FlatContentFactory.create(
            slug='test-content', site=None, content='test content')
        self.flat_site_content = FlatContentFactory.create(
            slug='test-content', site=self.site,
            content='test content with site')
        self.flat_content.save()
        self.flat_site_content.save()

    def test_cache_key(self):
        eq_('flatcontent_None_test-content',
            FlatContent.key_from_slug(self.flat_content.slug))
        eq_('flatcontent_1_test-content',
            FlatContent.key_from_slug(self.flat_site_content.slug,
                                      site_id=self.flat_site_content.site.id))

    def test_get(self):
        eq_('test content', FlatContent.get('test-content'))
        eq_('test content with site',
            FlatContent.get('test-content', site_id=self.site.id))
        site = SiteFactory.create()
        site.save()
        eq_('test content', FlatContent.get('test-content', site_id=site.id))

    def test_template_tag(self):
        resp = self.client.get(reverse('template_tag'))
        self.assertContains(resp, 'test content')

    def test_template_tag_with_site(self):
        resp = self.client.get(reverse('template_tag_with_site'))
        self.assertContains(resp, 'test content with site')

    def test_bad_arg_count(self):
        self.assertRaises(TemplateSyntaxError, self.client.get,
                          reverse('bad_arg_count'))

    def test_bad_second_arg(self):
        self.assertRaises(TemplateSyntaxError, self.client.get,
                          reverse('bad_second_arg'))
