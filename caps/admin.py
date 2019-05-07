from django.contrib import admin

from caps.models import LinkModel


@admin.register(LinkModel)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('checksum', 'long_url')
