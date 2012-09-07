from django.contrib import admin

from alias.models import Alias

class AliasAdmin(admin.ModelAdmin):
    list_display = ('text', 'aliased_type', 'aliased_object_id')

admin.site.register(Alias, AliasAdmin)
