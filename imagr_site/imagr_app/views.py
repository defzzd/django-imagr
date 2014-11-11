from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone

from django.views import generic

import datetime

import models



def front_page(request):

    # This view will send the user to the home_page if they're logged in
    # and the front_page again if not (a bandaid for the login/signup screen).

    if request.user.is_authenticated():
        return home_page(request)

    else:
        return render(request, 'imagr_app/front_page.html')

@login_required
def home_page(request):

    # if request.user.is_authenticated():

    # get_user_model() is how Django gives us the most flexibility
    # when redefining User classes. This will pull the settings.py
    # file's USER_AUTH_MODEL value, which is set by us, and use
    # the Model the string is referring to to function as the project's
    # base user. Calling get_user_model() here is like saying
    # ImagrUser (the model name, that is), except this is more general.
    imagr_user_object = get_object_or_404(get_user_model(),
                                          pk=request.user.id)

    user_id = imagr_user_object.id
    list_of_albums = get_list_or_404(models.Album,
                                     user=user_id)

    # list_of_albums=list_of_albums may need to be changed
    # to however context is handed through render()
    return render(request,
                  'imagr_app/home_page.html',
                  {'list_of_albums': list_of_albums
                   },)

    # else:
    #     return HttpResponseRedirect(reverse('imagr_app:front_page'))

@login_required
def album_page(request, album_id):

    # if request.user.is_authenticated():

    this_album = get_object_or_404(models.Album,
                                   pk=album_id)

    # User validation.
    # If someone is not logged in but enters a URL with an album ID,
    # the server will still try to server it up...
    # ... unless we tell it not to, if the permissions do not permit
    # this user to view this album. Permissions can be
    # 'public', 'private' and 'shared' -- so 'shared' should probably
    # cause a reference to the database that returns a list of users
    # this user has shared this album with.
    # But, that wasn't in the specifications, and there's no way to
    # view users other than self right now.
    # imagr_user_object = get_object_or_404(get_user_model(),
    #                                       pk=request.user.id)

    if ((this_album.published == 'public') or
        (this_album.user_id == request.user.id)):

        list_of_photos = this_album.photos.all()

        return render(request,
                      'imagr_app/album_page.html',
                      {'list_of_photos': list_of_photos,
                       'album_id': this_album.id
                       },
                      )
    else:
        return HttpResponseRedirect(reverse('imagr_app:front_page'))

    # else:
    #     return HttpResponseRedirect(reverse('imagr_app:front_page'))


@login_required
def photo_page(request, photo_id):

    # if request.user.is_authenticated():

    this_photo = get_object_or_404(models.Photo,
                                   pk=photo_id)

    # Provide this_photo with additional context:
    # A list of the IDs of every album it belongs to.
    # ...
    # This does not work for some reason; it returns one ID sometimes
    # outside of a list
    this_photo.album_id_list = []
    for each_album_id in [this_photo.Album_photos]:
        this_photo.album_id_list.append(each_album_id)

    if ((this_photo.published == 'public')
       or (this_photo.user_id == request.user.id)):
        # for photo in recent_self_photos:

        return render(request,
                      'imagr_app/photo_page.html',
                      {'this_photo': this_photo,
                       },)

    else:
        return HttpResponseRedirect(reverse('imagr_app:front_page'))


@login_required
def stream_page(request):
    # first, get the users' own recent photos
    # imagr_user_object = get_object_or_404(get_user_model(),
    #                                       pk=request.user.id)



    # filter_user_recent_photos =
    # list_of_photos = imagr_user_object.photo_set.get(user=request.user.id)

    # Photo.
    # now = timezone.now()
    # now - datetime.timedelta(days=1) <= self.date_uploaded <= now

    recent_self_photos = models.Photo.objects.filter(user=request.user.id).order_by('-date_uploaded')[:4]

    # Don't know if we need the following code here.
    # It gives album IDs to the stream_page for every photo
    # as part of each photo object.
    # for photo in recent_self_photos:
    #     photo.album_id_list = []
    #     for each_album_id in photo.Album_photos.id:
    #         photo.album_id_list.append(each_album_id)

    return render(request,
                  'imagr_app/stream_page.html',
                  {'recent_self_photos': recent_self_photos,
                   # 'recent_friend_photos': recent_friend_photos,
                   },
                  )



# Note to future developers and/or self:
# Triple quote blocks are NOT comments.
# They are strings.
# They will be loaded in memory as strings in a Python program during
# execution and, if not set to a variable, they will be garbage-collected.
# This makes them SEEM like comments, but they are NOT comments.
# Comments don't use memory, strings do.

# ++ A "front page" that shows anonymous users something nice to
# ++    encourage them to sign up (don't worry that we lack a means for
# ++    them to sign up yet.  We'll add that soon).

# ++ A "home page" that shows logged-in users a list of their albums,
# --    with a representative image from each album

# An "album page" that shows logged-in users a display of photos in
#     a single album
# A "photo page" that shows logged-in users a single photo along with
#     details about it.
# A "stream" page that shows users their most recent photos along
#     with recent photos uploaded by friends or those they are following.
