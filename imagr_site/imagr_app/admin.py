from django.contrib import admin
# This tells it to look in the same directory as the admin.py file:
from .models import Photo, Album, ImagrUser


class PhotoAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['title']}),
    #     (None, {'fields': ['description']}),
    #     ]

    # There isn't any 'create date' in the model.
    readonly_fields = ('date_uploaded', 'date_modified', 'date_published')

    # Reference:
    # http://stackoverflow.com/questions/2156114
    def name_url_field(self, obj):
        return '<a href="%s%s">%s</a>' % ('http://localhost:8000/admin/imagr_app/imagruser/', obj.user.id, obj.user.username)
    name_url_field.allow_tags = True
    name_url_field.short_description = 'Owner'

    # There also is no 'file size' in the model since we aren't hosting.
    list_display = ('title', 'image_url', 'name_url_field')

    # Reference:
    # https://docs.djangoproject.com/
    #     en/1.7/intro/tutorial02/#customize-the-admin-index-page
    # Let administrators sort the photos list by date_uploaded and user:
    list_filter = ['date_uploaded', 'user']

    # # Allow admins to search for individual entries by these fields:
    # search_fields = ['title']


class AlbumAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['title']}),
    #     (None, {'fields': ['description']}),
    #     ]

    # There isn't any 'create date' in the model.
    readonly_fields = ('date_uploaded', 'date_modified', 'date_published')

    # Reference:
    # http://stackoverflow.com/questions/2156114
    def name_url_field(self, obj):
        return '<a href="%s%s">%s</a>' % ('http://localhost:8000/admin/imagr_app/imagruser/', obj.user.id, obj.user.username)
    name_url_field.allow_tags = True
    name_url_field.short_description = 'Owner'

    list_display = ('title', 'name_url_field', 'date_modified', 'date_uploaded')

    list_filter = ['date_uploaded', 'user']


class ImagrUserAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['title']}),
    #     (None, {'fields': ['description']}),
    #     ]

    readonly_fields = ('password', 'date_joined', 'last_login')

    list_display = ('username', 'last_login', 'date_joined')

    # is_active is Django's User's is_active.
    # It is NOT our_is_active, which is useless...
    list_filter = ['date_joined', 'is_active']

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(ImagrUser, ImagrUserAdmin)


# # # # Specifications # # # #

# Using the documentation for the Django Admin (Links to an external site.),
#     make the following customizations for "Imagr":

# +- Display upload, create and modification dates in admin pages as
#        "read only" fields

# ++ Display the name of the owner of a Photo or Album in the list view
#        for each of those items

# -- Display the file size of a photo as a column of data in the list view
#        of Photos

# -- Allow administrators to click on the name of the owner of an Album or
#        Photo to jump to the edit page for that specific user.

# ++ Allow administrators to display all the photos created in a specific
#        time period.

# -- Allow administrators to search for albums or photos belonging to a
#        specific user by username, first name, last name or email address

# -- Allow administrators to search for users by username, first name, last
#        name or email address

# -- Allow administrators to display all photos uploaded that fall within
#        a particular upload size:
#            <= 1MB
#            <= 10 MB
#            <= 100 MB
#            > 100 MB





