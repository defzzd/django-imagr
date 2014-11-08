from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings

from django.views import generic

import models


def front_page(request):

    # This view will send the user to the home_page if they're logged in
    # and the front_page again if not (a bandaid for the login/signup screen).

    if request.user.is_authenticated():
        return home_page(request)

    else:
        return render(request, 'imagr_app/front_page.html')


def home_page(request):

    if request.user.is_authenticated():
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
                      {'list_of_albums': list_of_albums},
                      )

    else:
        return HttpResponseRedirect(reverse('imagr_app:front_page'))


def album_page(request, album_id):

    if request.user.is_authenticated():

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
        imagr_user_object = get_object_or_404(get_user_model(),
                                              pk=request.user.id)

        if this_album.published == 'public':
            if this_album.user_id == imagr_user_object.id:

                list_of_photos = this_album.photos.all()

                return render(request,
                              'imagr_app/album_page.html',
                              {'list_of_photos': list_of_photos},
                              )
        else:
            return HttpResponseRedirect(reverse('imagr_app:front_page'))

    else:
        return HttpResponseRedirect(reverse('imagr_app:front_page'))





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
