from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.template import TemplateSyntaxError
from django.test import TestCase
from django.utils import translation
from mock import patch
from nose.tools import eq_

from flatcontent.models import FlatContent
from .basefactory import FlatContentFactory, SiteFactory


class TestFlatContent(TestCase):

    def setUp(self):
        self.site = Site.objects.get()
        self.flat_content = FlatContentFactory(
            slug='test-content', site=None, content='test content')
        self.flat_site_content = FlatContentFactory.create(
            slug='test-content', site=self.site,
            content='test content with site')
        self.flat_content.save()
        self.flat_site_content.save()

    def test_cache_key(self):
        eq_('flatcontent_None_test-content_en-us',
            FlatContent.key_from_slug(self.flat_content.slug))
        eq_('flatcontent_1_test-content_en-us',
            FlatContent.key_from_slug(self.flat_site_content.slug,
                                      site_id=self.flat_site_content.site.id))
        translation.activate('tr')
        eq_('flatcontent_None_test-content_tr',
            FlatContent.key_from_slug(self.flat_content.slug))

    def test_get(self):
        eq_('test content', FlatContent.get('test-content'))
        eq_('test content with site',
            FlatContent.get('test-content', site_id=self.site.id))
        site = SiteFactory.create()
        site.save()
        eq_('test content', FlatContent.get('test-content', site_id=site.id))
        # Check that the items are now in the cache
        with patch.object(FlatContent.objects, 'get') as mock_objects_get:
            eq_('test content', FlatContent.get('test-content'))
            eq_(mock_objects_get.call_count, 0)

    def test_get_fallback(self):
        # Test the non site-specific fallback
        FlatContentFactory.create(
            slug='test-content2', site=None, content='test content2').save()
        eq_('test content2',
            FlatContent.get('test-content2', site_id=self.site.id))

    def test_get_not_found(self):
        # Test the flatcontent doesn't exist
        eq_('', FlatContent.get('not-found'))

    def test_get_with_context(self):
        """
        Check that get works with or without context, and no cache is used
        with context
        """
        flatcontent = FlatContentFactory.create(
            slug='test-tpl', site=None, content='Hi {{ name }}')

        assert FlatContent.get('test-tpl') == 'Hi '
        assert FlatContent.get('test-tpl', context={
            'name': 'Brad',
        }) == 'Hi Brad'

    def test_template_tag(self):
        resp = self.client.get(reverse('template_tag'))
        self.assertContains(resp, 'test content')

    def test_template_tag_as(self):
        resp = self.client.get(reverse('template_tag_as'))

        self.assertContains(resp, '<p>test content</p>')
        self.assertContains(resp, 'with first test content')
        self.assertContains(resp, 'with last test content')

    def test_template_tag_with_site(self):
        resp = self.client.get(reverse('template_tag_with_site'))
        self.assertContains(resp, 'test content with site')

    def test_template_tag_with_extra_ctx(self):
        FlatContentFactory(
            slug='test-content-with-extra-ctx',
            site=None,
            content='test content with {{ var1 }} {{ var2 }}',
        )

        resp = self.client.get(reverse('template_tag_with_extra_ctx'))

        self.assertContains(resp, 'test content with extra ctx')

    def test_template_tag_all_elements(self):
        FlatContentFactory(
            slug='test-content-all-elements',
            site=None,
            content='unused',
        )
        FlatContentFactory(
            slug='test-content-all-elements',
            site=self.site,
            content='test content with {{ var1 }} {{ var2 }}',
        )

        resp = self.client.get(reverse('template_tag_all_elements'))

        self.assertNotContains(resp, 'unused')
        self.assertContains(resp, '<p>test content with extra ctx1</p>')
        self.assertContains(resp, '<p>test content with extra ctx2</p>')
        self.assertContains(resp, '<p>test content with extra ctx3</p>')

    def test_missing_as(self):
        with self.assertRaises(TemplateSyntaxError) as tse:
            self.client.get(reverse('missing_as'))

        self.assertEqual(
            tse.exception.args[0],
            "The argument after 'as' should be a name for the context var",
        )

    def test_missing_with(self):
        with self.assertRaises(TemplateSyntaxError) as tse:
            self.client.get(reverse('missing_with'))

        self.assertEqual(
            tse.exception.args[0],
            "You must include key=value pairs after 'with'",
        )

    def test_bad_arg_count(self):
        with self.assertRaises(TemplateSyntaxError) as tse:
            self.client.get(reverse('bad_arg_count'))

        self.assertEqual(
            tse.exception.args[0],
            "The flatcontent tag requires 1 or 3+ arguments",
        )

    def test_bad_second_arg(self):
        with self.assertRaises(TemplateSyntaxError) as tse:
            self.client.get(reverse('bad_second_arg'))

        self.assertEqual(tse.exception.args[0], "Bad arguments supplied")
