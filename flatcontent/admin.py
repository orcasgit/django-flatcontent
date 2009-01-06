from django.contrib import admin

from flatcontent.models import FlatContent

class FlatContentAdmin(admin.ModelAdmin):
    list_display = ('slug', 'content')
    ordering = ('slug',)

admin.site.register(FlatContent, FlatContentAdmin)
