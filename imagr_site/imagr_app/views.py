from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone

import datetime

import models


def front_page(request):
    ''' The front_page shows anonymous users something
    nice to encourage them to sign up. '''

    # A bandaid for the login/signup screen.

    if request.user.is_authenticated():
        return home_page(request)

    else:
        return render(request, 'imagr_app/front_page.html')


@login_required
def home_page(request):
    ''' The home_page shows logged-in users a list of their
    albums, with a representative image from each album. '''

    # get_user_model() is how Django gives us the most flexibility
    # when redefining User classes. This will pull the settings.py
    # file's USER_AUTH_MODEL value, which is set by us, and use
    # the Model the string is referring to to function as the project's
    # base user. Calling get_user_model() here is like saying
    # models.ImagrUser (the model name, that is), except this is more general.
    imagr_user_object = get_object_or_404(get_user_model(),
                                          pk=request.user.id)

    user_id = imagr_user_object.id
    list_of_albums = get_list_or_404(models.Album,
                                     user=user_id)

    return render(request,
                  'imagr_app/home_page.html',
                  {'list_of_albums': list_of_albums
                   },)


@login_required
def album_page(request, album_id):
    '''The album_page shows logged-in users
    a display of photos in a single album.'''

    this_album = get_object_or_404(models.Album,
                                   pk=album_id)

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


@login_required
def photo_page(request, photo_id):
    ''' The photo_page shows logged-in users a
    single photo along with details about it. '''

    this_photo = get_object_or_404(models.Photo,
                                   pk=photo_id)

    if ((this_photo.published == 'public')
       or (this_photo.user_id == request.user.id)):

        return render(request,
                      'imagr_app/photo_page.html',
                      {'this_photo': this_photo,
                       },)

    else:
        return HttpResponseRedirect(reverse('imagr_app:front_page'))


@login_required
def stream_page(request):
    ''' The stream_page shows users their most recent photos along
    with recent photos uploaded by those they are following. '''

    recent_self_photos = models.Photo.objects.filter(user=request.user.id).order_by('-date_uploaded')[:4]

    imagr_user_object = get_object_or_404(get_user_model(),
                                          pk=request.user.id)

    recent_friend_photos = []

    for each_photo in models.Photo.objects.exclude(published="private").order_by('-date_uploaded')[:4]:

        for each_user_object in each_photo.user.followers.all():

            if request.user.id == each_user_object.id:

                recent_friend_photos.append(each_photo)

    # To avoid having to parse this list of friends' shareable photos
    # (which we can't easily do via Django, because we've already removed
    # them from the Manager with its exclude() and order_by() methods)
    # we will instead take a random sample of a user's friends' recent photos:
    import random
    recent_friend_photos = random.sample(recent_friend_photos, min(len(recent_friend_photos), 4))

    return render(request,
                  'imagr_app/stream_page.html',
                  {'recent_self_photos': recent_self_photos,
                   'recent_friend_photos': recent_friend_photos,
                   },
                  )
