from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone

import datetime

import models
import forms


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

    # Used when altering forms' querysets, below, after form creation:
    imagr_user_object = get_object_or_404(get_user_model(),
                                          pk=request.user.id)


    context_dictionary = {}
    context_dictionary['this_album'] = this_album

    if ((this_album.published == 'public') or
       (this_album.user_id == request.user.id)):

        context_dictionary['list_of_photos'] = this_album.photos.all()

    # If the user is not logged in and the album is not public, goto front_page
    else:
        return HttpResponseRedirect(reverse('imagr_app:front_page'))

    # Editing of albums is now done on the album_page itself.
    invalidation_string = ''
    context_dictionary['invalidation_string'] = invalidation_string

    if (request.method == 'POST') and (request.user.id == this_album.user_id):

        this_album_edit_form = forms.EditAlbumForm(request.POST)
        if this_album_edit_form.is_valid():
            #print(str(this_album_edit_form.cleaned_data))

            if this_album_edit_form.cleaned_data['title']:
                this_album.title = this_album_edit_form.cleaned_data['title']

            if this_album_edit_form.cleaned_data['description']:
                this_album.description = this_album_edit_form.cleaned_data['description']

            if this_album_edit_form.cleaned_data['published']:
                this_album.published = this_album_edit_form.cleaned_data['published']

            if this_album_edit_form.cleaned_data['cover']:
                this_album.cover = this_album_edit_form.cleaned_data['cover']

            if this_album_edit_form.cleaned_data['photos']:
                # "Editing" the album can mean removing photos.
                # Hopefully the album form will pre-select photos already
                # inside the album, so we can clear all of them and re-add
                # from whatever was submitted with the form.
                this_album.photos.clear()
                for each_photo in this_album_edit_form.cleaned_data['photos']:
                    this_album.photos.add(each_photo)

            this_album.save()

            # Violating DRY here because this needs to be refreshed
            # after the album has been saved so the album view page
            # (which we redirect to after editing) reflects the
            # newly-edited data.
            #initial_data_photos_list = this_album.photos.filter(user=request.user.id).exclude(published='private')

            initial_data = {'title': this_album.title,
                            'description': this_album.description,
                            'published': this_album.published,
                            'cover': this_album.cover.pk}
            print initial_data

            this_album_edit_form = forms.EditAlbumForm(initial_data)
            # 'public', because private would allow public albums to have private covers, and shared would be hard to implement:
            #this_album_edit_form.fields.fields['cover'].queryset = models.Photo.objects.filter(user=imagr_user_object, published='public')

            context_dictionary['this_album_edit_form'] = this_album_edit_form
            invalidation_string = 'Album successfully updated.'
            context_dictionary['invalidation_string'] = invalidation_string

            return render(request,
                          'imagr_app/album_page.html',
                          context_dictionary)

        else:
            invalidation_string = 'Invalid entry: all fields required.'

    # If a GET (or any other method), create a blank form.
    # NOTE: This must check for request.user.id == this_photo.user_id, or else
    # non-users who can see the photo would be given an edit form, even
    # though they couldn't actually submit it.
    if (request.user.id == this_album.user_id):

        # Violating DRY here because this needs to be refreshed
        # after the album has been saved so the album view page
        # (which we redirect to after editing) reflects the
        # newly-edited data.
        #initial_data_photos_list = this_album.photos.filter(user=request.user.id).exclude(published='private')

        initial_data = {'title': this_album.title,
                        'description': this_album.description,
                        'published': this_album.published,
                        'cover': this_album.cover.pk}  # initial_data_photos_list}

        this_album_edit_form = forms.EditAlbumForm(initial_data)

        context_dictionary['this_album_edit_form'] = this_album_edit_form
        context_dictionary['invalidation_string'] = invalidation_string

    return render(request,
                  'imagr_app/album_page.html',
                  context_dictionary)


@login_required
def photo_page(request, photo_id):
    ''' The photo_page shows logged-in users a
    single photo along with details about it. '''

    this_photo = get_object_or_404(models.Photo,
                                   pk=photo_id)

    context_dictionary = {}

    if ((this_photo.published == 'public')
       or (this_photo.user_id == request.user.id)):

        context_dictionary['this_photo'] = this_photo

    # If the user is not logged in and the photo is not public, send em back.
    else:
        return HttpResponseRedirect(reverse('imagr_app:front_page'))

    # Editing of photos is now done on the photo_page itself.
    invalidation_string = ''
    context_dictionary['invalidation_string'] = invalidation_string

    if (request.method == 'POST') and (request.user.id == this_photo.user_id):

        photo_form = forms.EditPhotoForm(request.POST)

        if photo_form.is_valid():
            print(str(photo_form.cleaned_data))

            if photo_form.cleaned_data['title']:
                this_photo.title = photo_form.cleaned_data['title']

            if photo_form.cleaned_data['description']:
                this_photo.description = photo_form.cleaned_data['description']

            if photo_form.cleaned_data['published']:
                this_photo.published = photo_form.cleaned_data['published']

            if photo_form.cleaned_data['image_url']:
                this_photo.image_url = photo_form.cleaned_data['image_url']

            this_photo.save()

            # Violating DRY here so we can update the defaults after updating the model after submitting a post... yeah.
            initial_data = {'title': this_photo.title,
                            'description': this_photo.description,
                            'published': this_photo.published,
                            'image_url': this_photo.image_url}

            this_photo_edit_form = forms.EditPhotoForm(initial_data)
            context_dictionary['this_photo_edit_form'] = this_photo_edit_form
            invalidation_string = 'Photo successfully updated.'
            context_dictionary['invalidation_string'] = invalidation_string

            return render(request,
                          'imagr_app/photo_page.html',
                          context_dictionary)

        else:
            invalidation_string = 'Invalid entry. Image URL must be a valid URL.'
    # If a GET (or any other method), create a blank form.
    # NOTE: This must check for request.user.id == this_photo.user_id, or else
    # non-users who can see the photo would be given an edit form, even
    # though they couldn't actually submit it.
    if (request.user.id == this_photo.user_id):

        initial_data = {'title': this_photo.title,
                        'description': this_photo.description,
                        'published': this_photo.published,
                        'image_url': this_photo.image_url}

        this_photo_edit_form = forms.EditPhotoForm(initial_data)
        context_dictionary['this_photo_edit_form'] = this_photo_edit_form
        context_dictionary['invalidation_string'] = invalidation_string

    return render(request,
                  'imagr_app/photo_page.html',
                  context_dictionary)


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


@login_required
def add_photo(request):

    invalidation_string = ''

    if request.method == 'POST':

        photo_form = forms.CreatePhotoForm(request.POST)

        if photo_form.is_valid():
            print(str(photo_form.cleaned_data))
            imagr_user_object = get_object_or_404(get_user_model(),
                                                  pk=request.user.id)
            new_photo = models.Photo.objects.create(
                user=imagr_user_object,
                title=photo_form.cleaned_data['title'],
                description=photo_form.cleaned_data['description'],
                published=photo_form.cleaned_data['published'],
                image_url=photo_form.cleaned_data['image_url'])


            new_photo.save()

            return HttpResponseRedirect(reverse('imagr_app:home_page'))

        else:
            invalidation_string = 'Invalid entry. All fields required, image URL must be a valid URL.'

    # If a GET (or any other method), create a blank form.
    else:
        photo_form = forms.CreatePhotoForm()

    return render(request, 'imagr_app/add_photo.html', {
        'photo_form': photo_form,
        'invalidation_string': invalidation_string,
        })


@login_required
def add_album(request):

    invalidation_string = ''

    if request.method == 'POST':

        album_form = forms.CreateAlbumForm(request.POST)

        if album_form.is_valid():
            print(str(album_form.cleaned_data))
            imagr_user_object = get_object_or_404(get_user_model(),
                                                  pk=request.user.id)
            new_album = models.Album.objects.create(
                user=imagr_user_object,
                title=album_form.cleaned_data['title'],
                description=album_form.cleaned_data['description'],
                published=album_form.cleaned_data['published'],
                cover=album_form.cleaned_data['cover'],
                # You can't add the form's photos to the new Album object
                # here, because a ManyToMany field cannot be given data
                # upon creation of a new model instance.
                # photos=album_form.cleaned_data['photos']
                )
            # Instead you must unpack the list and fill the photos field
            # after the instance has been created:
            photos_list = album_form.cleaned_data['photos']
            for each_photo in photos_list:
                new_album.photos.add(each_photo)
            new_album.save()
            # The args parameter is how we pass a variable to reverse():
            return HttpResponseRedirect(reverse('imagr_app:album_page', args=[new_album.id]))

        else:
            invalidation_string = 'Invalid entry. All fields required, image URL must be a valid URL.'

    # If a GET (or any other method), create a blank form.
    else:
        album_form = forms.CreateAlbumForm()

    return render(request, 'imagr_app/add_album.html', {
        'album_form': album_form,
        'invalidation_string': invalidation_string,
        })














