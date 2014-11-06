from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings

from django.views import generic

import models


def front_page(request):

    return render(request, 'imagr_app/front_page.html')


def home_page(request):

    if request.user.is_authenticated():

        imagr_user_object = get_object_or_404(settings.AUTH_USER_MODEL,
                                              pk=request.user.id)

        user_id = imagr_user_object.id
        list_of_albums = get_list_or_404(models.Album,
                                         user=user_id)

        # list_of_albums=list_of_albums may need to be changed
        # to however context is handed through render()
        return render(request,
                      'imagr_app/home_page.html',
                      list_of_albums=list_of_albums)

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
