from django.core.urlresolvers import reverse
from django.test import TestCase
from nose.tools import eq_

from flatcontent.models import FlatContent
from .basefactory import FlatContentFactory


class TestFlatContent(TestCase):

    def test_template_tag(self):
        flatcontent = FlatContentFactory.create(
            slug='test-content', content='test content')
        flatcontent.save()
        eq_(FlatContent.objects.count(), 1)
        resp = self.client.get(reverse('show_flatcontent'))
        self.assertContains(resp, 'test content')
