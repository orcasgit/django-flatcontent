from django.core.cache import cache
from django.db import models

class FlatContent(models.Model):
    slug = models.SlugField(max_length=255, unique=True, help_text='The name by which the template author retrieves this content.')
    content = models.TextField()

    class Meta:
        verbose_name_plural = 'flat content'

    def __unicode__(self):
        return self.slug

    def save(self):
        super(FlatContent, self).save()
        cache.delete(self.key_from_slug(self.slug))

    def delete(self):
        cache.delete(self.key_from_slug(self.slug))
        super(FlatContent, self).delete()

    # Helper method to get key for caching
    def key_from_slug(slug):
        return 'flatcontent_%s' % (slug)
    key_from_slug = staticmethod(key_from_slug)

    # Class method with caching
    def get(cls, slug):
        """
        Checks if key is in cache, otherwise performs database lookup and
        inserts into cache.
        """
        key = cls.key_from_slug(slug)
        cache_value = cache.get(key)
        if cache_value:
            return cache_value

        try:
            fc = cls.objects.get(slug=slug)
        except cls.DoesNotExist:
            return ''
        cache.set(key, fc.content)
        return fc.content
    get = classmethod(get)

