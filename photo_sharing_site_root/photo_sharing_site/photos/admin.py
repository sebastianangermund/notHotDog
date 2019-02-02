from django.contrib import admin

from photo_sharing_site.photos.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
	list_display = ('owner', 'uploaded')
	list_filter = ('owner',)
