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
    list_of_albums = models.Album.objects.filter(user=user_id)

    return render(request,
                  'imagr_app/home_page.html',
                  {'list_of_albums': list_of_albums
                   },)


@login_required
def album_page(request, album_id):
    ''' The album_page shows logged-in users
    a display of photos in a single album
    and allows logged-in users the ability
    to edit the album's details. '''

    this_album = get_object_or_404(models.Album, pk=album_id)
    this_user = get_object_or_404(get_user_model(), pk=request.user.id)

    context_dictionary = {}
    context_dictionary['this_album'] = this_album

    # NOTE: The final possible condition, the 'shared' one, checks to see
    # if the user who owns this album has shared it and the user who is looking
    # at the album is following the user who owns the album.
    # This is like checking to see if you're following someone on Twitter,
    # except if you aren't electing to follow them, you can't see their stuff.
    if ((this_album.published == 'public')
        or (this_album.user_id == request.user.id)
            or ((this_album.published == 'shared')
                and (this_user.following.filter(pk=this_album.user_id)[0].id
                     == this_album.user_id))):

        context_dictionary['list_of_photos'] = this_album.photos.all()

    # If the user is not logged in and the album is not public, goto front_page
    else:
        return HttpResponseRedirect(reverse('imagr_app:front_page'))

    # Editing of albums is now done on the album_page itself.
    context_string = ''
    context_dictionary['context_string'] = context_string

    if (request.method == 'POST') and (request.user.id == this_album.user_id):

        this_album_edit_form = forms.EditAlbumForm(request.POST)
        if this_album_edit_form.is_valid():

            if this_album_edit_form.cleaned_data['title']:
                this_album.title = this_album_edit_form.cleaned_data['title']

            if this_album_edit_form.cleaned_data['description']:
                this_album.description \
                    = this_album_edit_form.cleaned_data['description']

            if this_album_edit_form.cleaned_data['published']:
                this_album.published \
                    = this_album_edit_form.cleaned_data['published']

            if this_album_edit_form.cleaned_data['cover']:
                this_album.cover \
                    = this_album_edit_form.cleaned_data['cover']

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

            initial_data = {'title': this_album.title,
                            'description': this_album.description,
                            'published': this_album.published,
                            'cover': this_album.cover.pk,
                            'photos': this_album.photos.all()}

            this_album_edit_form = forms.EditAlbumForm(initial_data)

            context_dictionary['this_album_edit_form'] = this_album_edit_form
            context_string = 'Album successfully updated.'
            context_dictionary['context_string'] = context_string

            return render(request,
                          'imagr_app/album_page.html',
                          context_dictionary)

        else:
            context_string = 'Invalid entry: all fields required.'

    # If a GET (or any other method), create a blank form.
    # NOTE: This must check for request.user.id == this_photo.user_id, or else
    # non-users who can see the photo would be given an edit form, even
    # though they couldn't actually submit it.
    if (request.user.id == this_album.user_id):

        # Violating DRY here because this needs to be refreshed
        # after the album has been saved so the album view page
        # (which we redirect to after editing) reflects the
        # newly-edited data.

        initial_data = {'title': this_album.title,
                        'description': this_album.description,
                        'published': this_album.published,
                        'cover': this_album.cover.pk,
                        'photos': this_album.photos.all()}

        this_album_edit_form = forms.EditAlbumForm(initial_data)

        context_dictionary['this_album_edit_form'] = this_album_edit_form
        context_dictionary['context_string'] = context_string

    return render(request,
                  'imagr_app/album_page.html',
                  context_dictionary)


@login_required
def photo_page(request, photo_id):
    ''' The photo_page shows logged-in users a
    single photo along with details about it
    and allows logged-in users the ability to
    edit the photo's details. '''

    this_photo = get_object_or_404(models.Photo, pk=photo_id)
    this_user = get_object_or_404(get_user_model(), pk=request.user.id)

    context_dictionary = {}

    # NOTE: The final possible condition, the 'shared' one, checks to see
    # if the user who owns this photo has shared it and the user who is looking
    # at the photo is following the user who owns the photo.
    # This is like checking to see if you're following someone on Twitter,
    # except if you aren't electing to follow them, you can't see their stuff.
    if ((this_photo.published == 'public')
        or (this_photo.user_id == request.user.id)
            or ((this_photo.published == 'shared')
                and (this_user.following.filter(pk=this_photo.user_id)[0].id
                     == this_photo.user_id))):

        context_dictionary['this_photo'] = this_photo

    # If the user is not logged in and the photo is not public, send em back.
    else:
        return HttpResponseRedirect(reverse('imagr_app:front_page'))

    # Editing of photos is now done on the photo_page itself.
    context_string = ''
    context_dictionary['context_string'] = context_string

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

            # Violating DRY here so we can update the defaults after
            # updating the model after submitting a post... yeah.
            initial_data = {'title': this_photo.title,
                            'description': this_photo.description,
                            'published': this_photo.published,
                            'image_url': this_photo.image_url}

            this_photo_edit_form = forms.EditPhotoForm(initial_data)
            context_dictionary['this_photo_edit_form'] = this_photo_edit_form
            context_string = 'Photo successfully updated.'
            context_dictionary['context_string'] = context_string

            return render(request,
                          'imagr_app/photo_page.html',
                          context_dictionary)

        else:
            context_string = 'Error: Image URL must be a valid URL.'

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
        context_dictionary['context_string'] = context_string

    return render(request,
                  'imagr_app/photo_page.html',
                  context_dictionary)


@login_required
def stream_page(request):
    ''' The stream_page shows users their most recent photos along
    with recent photos uploaded by those they are following. '''

    recent_self_photos = models.Photo.objects.filter(
        user=request.user.id).order_by('-date_uploaded')[:4]

    recent_friend_photos = []

    ordered_shared_nonprivate_photos = models.Photo.objects.exclude(
        published="private").order_by('-date_uploaded')[:4]

    for each_photo in ordered_shared_nonprivate_photos:

        for each_user_object in each_photo.user.followers.all():

            if request.user.id == each_user_object.id:

                recent_friend_photos.append(each_photo)

    # To avoid having to parse this list of friends' shareable photos
    # (which we can't easily do via Django, because we've already removed
    # them from the Manager with its exclude() and order_by() methods)
    # we will instead take a random sample of a user's friends' recent photos:
    import random
    recent_friend_photos = random.sample(recent_friend_photos,
                                         min(len(recent_friend_photos), 4)
                                         )

    return render(request,
                  'imagr_app/stream_page.html',
                  {'recent_self_photos': recent_self_photos,
                   'recent_friend_photos': recent_friend_photos})


@login_required
def add_photo(request):
    ''' The add_photo page allows users to add a photo to the site. '''

    context_string = ''

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
            context_string = 'Invalid entry. URL must be a valid URL.'

    # If a GET (or any other method), create a blank form.
    else:
        photo_form = forms.CreatePhotoForm()

    return render(request, 'imagr_app/add_photo.html', {
                  'photo_form': photo_form,
                  'context_string': context_string,
                  })


@login_required
def add_album(request):
    ''' The add_album page allows users to add an album to the
    site and associate it with a selection of their photos. '''

    context_string = ''

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
            return HttpResponseRedirect(reverse('imagr_app:album_page',
                                                args=[new_album.id]))

        else:
            context_string = 'Invalid entry. All fields required.'

    # If a GET (or any other method), create a blank form.
    else:
        album_form = forms.CreateAlbumForm()

    return render(request, 'imagr_app/add_album.html', {
                  'album_form': album_form,
                  'context_string': context_string,
                  })


@login_required
def delete_photo(request, photo_id):
    ''' The delete_photo view allows users to delete photos they own. '''

    this_photo = get_object_or_404(models.Photo,
                                   pk=photo_id)

    # Note: This check is critically distinct from
    # what @login_required guarantees us.
    if request.user.id == this_photo.user_id:

        models.Photo.objects.get(pk=photo_id).delete()

    return HttpResponseRedirect(reverse('imagr_app:home_page'))


@login_required
def delete_album(request, album_id):
    ''' The delete_album view allows users to delete
    photos they own without deleting photos. '''

    this_album = get_object_or_404(models.Album,
                                   pk=album_id)

    # Note: This check is critically distinct from
    # what @login_required guarantees us.
    if request.user.id == this_album.user_id:

        models.Album.objects.get(pk=album_id).delete()

    return HttpResponseRedirect(reverse('imagr_app:home_page'))


@login_required
def follow_page(request):
    '''The follow_page shows logged-in users
    a display of users they are following and
    allows them to follow and unfollow users.'''

    # Used when altering forms' querysets below, after form creation:
    this_user = get_object_or_404(get_user_model(), pk=request.user.id)

    context_dictionary = {}
    # context_dictionary['this_user'] = imagr_user_object
    # Listify it for the templating language:
    context_dictionary['following'] = this_user.following.all()

    followers = models.ImagrUser.objects.filter(following=this_user)
    context_dictionary['followers'] = followers

    context_string = ''

    if request.method == 'POST':

        follow_form = forms.EditFollowedUsersForm(request.POST)
        if follow_form.is_valid():
            following = follow_form.cleaned_data['following']
            if following:
                this_user.following.clear()
                for each_followed_user in following:
                    this_user.following.add(each_followed_user)

            this_user.save()

            # Violating DRY here because this needs to be refreshed
            # after the album has been saved so the album view page
            # (which we redirect to after editing) reflects the
            # newly-edited data.
            initial_data = {'following': this_user.following.all()}

            follow_form = forms.EditFollowedUsersForm(initial_data)

            context_dictionary['follow_form'] = follow_form
            context_string = 'Updated your followed users list.'
            context_dictionary['context_string'] = context_string

            return render(request,
                          'imagr_app/follow_page.html',
                          context_dictionary)

        else:
            context_string = 'Invalid entry, reason unknown.'

    # If a GET (or any other method), create a blank form.
    # Actually, just hand them a blank form every time.
    # It turns out there's no reason not to.
    initial_data = {'following': this_user.following.all()}

    follow_form = forms.EditFollowedUsersForm(initial_data)

    context_dictionary['follow_form'] = follow_form

    context_dictionary['context_string'] = context_string

    return render(request,
                  'imagr_app/follow_page.html',
                  context_dictionary)


@login_required
def history_page(request):
    ''' The history_page shows logged-in users a
    chronologically-ordered list of their photos. '''

    imagr_user_object = get_object_or_404(get_user_model(),
                                          pk=request.user.id)

    # Might be able to alt-cmd-f all copies of this line into request.user.id
    user_id = imagr_user_object.id

    list_of_photos = models.Photo.objects.filter(
        user=user_id).order_by('-date_uploaded')[:20]
    list_of_albums = models.Album.objects.filter(
        user=user_id).order_by('-date_uploaded')[:20]

    return render(request,
                  'imagr_app/history_page.html',
                  {'list_of_photos': list_of_photos,
                   'list_of_albums': list_of_albums})
