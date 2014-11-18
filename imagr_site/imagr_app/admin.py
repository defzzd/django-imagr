from django.contrib import admin
# This tells it to look in the same directory as the admin.py file:
from .models import Photo, Album, ImagrUser


class PhotoAdmin(admin.ModelAdmin):

    # There is no 'create date' in the specs, but there are these...
    readonly_fields = ('date_uploaded', 'date_modified', 'date_published')

    # Reference:
    # http://stackoverflow.com/questions/2156114
    def name_url_field(self, obj):
        constructed_url_tag = '<a href="%s%s">%s</a>' \
            % ('http://localhost:8000/admin/imagr_app/imagruser/',
               obj.user.id,
               obj.user.username)
        return constructed_url_tag
    name_url_field.allow_tags = True
    name_url_field.short_description = 'Owner'

    # There also is no 'file size' in the model since we aren't hosting.
    list_display = ('title', 'image_url', 'name_url_field')

    # Reference:
    # https://docs.djangoproject.com/
    #     en/1.7/intro/tutorial02/#customize-the-admin-index-page
    # Let administrators sort the photos list by date_uploaded and user:
    list_filter = ['date_uploaded']

    # Figured this out with the help of this StackOverflow post's responses
    # and a little bit of intuition:
    # http://stackoverflow.com/questions/11754877
    #        /troubleshooting-related-field-has-invalid-lookup-icontains
    # ...
    # 'user__email_address' gives me "does not support nested lookups"
    # BUT 'user__email' works fine. I forgot to check the AbstractUser model
    # for its email field, which is simply named "email".
    search_fields = ['user__username',
                     'user__email',
                     'user__first_name',
                     'user__last_name']


class AlbumAdmin(admin.ModelAdmin):

    readonly_fields = ('date_uploaded', 'date_modified', 'date_published')

    # Reference:
    # http://stackoverflow.com/questions/2156114
    def name_url_field(self, obj):
        constructed_url_tag = '<a href="%s%s">%s</a>' \
            % ('http://localhost:8000/admin/imagr_app/imagruser/',
               obj.user.id,
               obj.user.username)
        return constructed_url_tag
    name_url_field.allow_tags = True
    name_url_field.short_description = 'Owner'

    list_display = ('title',
                    'name_url_field',
                    'date_modified',
                    'date_uploaded')

    list_filter = ['date_uploaded']
    search_fields = ['user__username',
                     'user__email',
                     'user__first_name',
                     'user__last_name']


class ImagrUserAdmin(admin.ModelAdmin):

    readonly_fields = ('password',
                       'date_joined',
                       'last_login')

    list_display = ('username',
                    'last_login',
                    'date_joined')

    list_filter = ['date_joined',
                   'is_active']

    search_fields = ['username',
                     'email',
                     'first_name',
                     'last_name']


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(ImagrUser, ImagrUserAdmin)
