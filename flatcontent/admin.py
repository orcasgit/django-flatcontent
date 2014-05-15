from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from flatcontent.models import FlatContent


class FlatContentResource(resources.ModelResource):
    class Meta:
        model = FlatContent


class FlatContentAdmin(ImportExportModelAdmin):
    list_display = ('slug', 'site', 'content',)
    ordering = ('slug', 'site',)
    resource_class = FlatContentResource


admin.site.register(FlatContent, FlatContentAdmin)
