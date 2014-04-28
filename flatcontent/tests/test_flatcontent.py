from django.core.urlresolvers import reverse
from django.template import TemplateSyntaxError
from django.test import TestCase
from nose.tools import eq_

from flatcontent.models import FlatContent
from .basefactory import FlatContentFactory


class TestFlatContent(TestCase):

    def setUp(self):
        self.flat_content = FlatContentFactory.create(
            slug='test-content', content='test content')
        self.flat_content.save()

    def test_template_tag(self):
        resp = self.client.get(reverse('template_tag'))
        self.assertContains(resp, 'test content')

    def test_bad_arg_count(self):
        self.assertRaises(TemplateSyntaxError, self.client.get,
                          reverse('bad_arg_count'))

    def test_bad_second_arg(self):
        self.assertRaises(TemplateSyntaxError, self.client.get,
                          reverse('bad_second_arg'))
        
