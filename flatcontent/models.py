from django.db import models

class FlatContent(models.Model):
   slug = models.SlugField(max_length=255, unique=True, help_text='The name by which the template author retrieves this content.')
   content = models.TextField()

   def __unicode__(self):
       return self.slug

   class Meta:
       verbose_name_plural = 'flat content'
