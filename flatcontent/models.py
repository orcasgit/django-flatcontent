from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db import models
from django.utils import translation
from templatefield.fields import TemplateTextField
from templatefield.managers import RenderTemplateManager


class FlatContent(models.Model):
    slug = models.SlugField(max_length=255, unique=False,
                            help_text='The name by which the template author '
                                      'retrieves this content.')
    site = models.ForeignKey(Site, blank=True, null=True)
    content = TemplateTextField()

    default = models.Manager()
    objects = RenderTemplateManager()

    class Meta:
        unique_together = ('slug', 'site',)
        verbose_name_plural = 'flat content'

    def __unicode__(self):
        return self.slug

    def save(self, *args, **kwargs):
        super(FlatContent, self).save(*args, **kwargs)
        cache.delete(self.key_from_slug(
            self.slug, site_id=self.site.id if self.site else None))

    def delete(self):
        cache.delete(self.key_from_slug(
            self.slug, site_id=self.site.id if self.site else None))
        super(FlatContent, self).delete()

    # Helper method to get key for caching
    def key_from_slug(slug, site_id=None):
        lang = translation.get_language()
        return 'flatcontent_%s_%s_%s' % (site_id, slug, lang)
    key_from_slug = staticmethod(key_from_slug)

    # Class method with caching
    @classmethod
    def get(cls, slug, site_id=None, context=None):
        """
        Checks if key is in cache, otherwise performs database lookup and
        inserts into cache.
        """
        key, cache_value = cls._get_cached(slug, site_id, context)
        if cache_value:
            return cache_value

        manager = cls.objects.with_context(context or {})
        try:
            fc = manager.get(slug=slug, site=site_id)
        except cls.DoesNotExist:
            try:
                # Fallback to the non-site specific flatcontent
                key, cache_value = cls._get_cached(slug, context=context)
                if cache_value:
                    return cache_value
                fc = manager.get(slug=slug, site=None)
            except:
                return ''
        if not context:
            cache.set(key, fc.content)
        return fc.content

    @classmethod
    def _get_cached(cls, slug, site_id=None, context=None):
        key = cls.key_from_slug(slug, site_id=site_id)
        cache_value = None if context else cache.get(key)
        return key, cache_value
