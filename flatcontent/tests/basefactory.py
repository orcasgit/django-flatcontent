import factory

from django.contrib.sites.models import Site
from flatcontent.models import FlatContent


class FlatContentFactory(factory.Factory):
    FACTORY_FOR = FlatContent

class SiteFactory(factory.Factory):
    FACTORY_FOR = Site
