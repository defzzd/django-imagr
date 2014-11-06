from django.contrib import admin
# This tells it to look in the same directory as the admin.py file:
from .models import Photo, Album, ImagrUser

admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(ImagrUser)
