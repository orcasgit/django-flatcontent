import factory

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from flatcontent.models import FlatContent


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: 'username{0}'.format(n))
    password = 'password'
    email = factory.Sequence(lambda n: 'email{0}@example.com'.format(n))

    @classmethod
    def _prepare(cls, create, **kwargs):
        plain_password = kwargs.pop('password')
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        user.set_password(plain_password)
        user.save()
        return user


class FlatContentFactory(factory.Factory):
    FACTORY_FOR = FlatContent

    slug = factory.Sequence(lambda n: 'slug{0}'.format(n))
    content = factory.Sequence(lambda n: 'content{0}'.format(n))

class SiteFactory(factory.Factory):
    FACTORY_FOR = Site
