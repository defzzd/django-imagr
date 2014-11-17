from django.contrib import admin
# This tells it to look in the same directory as the admin.py file:
from .models import Photo, Album, ImagrUser


# class PhotoAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['title']}),
#         (None, {'fields': ['description']}),
#         ]
#     list_display = ('title', 'image_url')
#     search_fields = ['title']

# admin.site.register(Photo, PhotoAdmin)

admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(ImagrUser)
