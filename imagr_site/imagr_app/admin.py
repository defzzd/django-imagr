from django.contrib import admin
# This tells it to look in the same directory as the admin.py file:
from .models import Photo, Album, ImagrUser


class PhotoAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['title']}),
    #     (None, {'fields': ['description']}),
    #     ]

    # There isn't any 'create date' in the model.
    readonly_fields = ('date_uploaded', 'date_modified')
    # There also is no 'file size' in the model since we aren't hosting.
    list_display = ('title', 'image_url')

    # Reference:
    # https://docs.djangoproject.com/
    #     en/1.7/intro/tutorial02/#customize-the-admin-index-page

    # # Allow admins to search for individual entries by these fields:
    # search_fields = ['title']


class AlbumAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['title']}),
    #     (None, {'fields': ['description']}),
    #     ]

    # There isn't any 'create date' in the model.
    readonly_fields = ('date_uploaded', 'date_modified')

    list_display = ('title', 'user', 'date_modified', 'date_uploaded')


class ImagrUserAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {'fields': ['title']}),
    #     (None, {'fields': ['description']}),
    #     ]

    readonly_fields = ('password', 'date_joined', 'last_login')

    list_display = ('username', 'last_login', 'date_joined')


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

# -- Allow administrators to display all the photos created in a specific
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





