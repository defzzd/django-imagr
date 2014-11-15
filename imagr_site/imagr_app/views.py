from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import get_object_or_404
from models import ImagrUser, Photo, Album
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from forms import AlbumForm, PhotoForm
import datetime


def front_page(request):
    if request.user.is_authenticated():
        # This may need to call HttpResponseRequest() instead of render()
        return home_page(request)
    else:
        #We'll fix this later, once we've decided what to do with the front page
        return home_page(request)
        #return HttpResponseRedirect('imagr_app/front_page.html')


@login_required
def home_page(request):
    current_user = get_object_or_404(get_user_model(), pk=request.user.id)
    user_albums = Album.objects.filter(user=current_user.id)
    context = {'current_user': current_user, 'user_albums': user_albums}
    return render(request, 'imagr_app/home_page.html', context)


@login_required
def album_page(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    photos = album.photos.all()
    context = {'album': album, 'photos': photos}
    return render(request, 'imagr_app/album.html', context)


@login_required
def photo_page(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    context = {'photo': photo}
    return render(request, 'imagr_app/photo.html', context)


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            new_photo = Photo.objects.create(
                user=get_object_or_404(get_user_model(), pk=request.user.id),
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                published=form.cleaned_data['published'],
                date_published=datetime.datetime.now(),
                photo_data=form.cleaned_data['photo_data'])
            new_photo.save()

            return HttpResponseRedirect(reverse('imagr_app:stream'))
    else:
        form = PhotoForm()
    
    context = {'photo_form': form}
    return render(request, 'imagr_app/submit_photo.html', context)


@login_required
def stream(request):
    recent_user_photos = Photo.objects.filter(user=request.user.id).order_by('-date_uploaded')[:4]
    user = get_object_or_404(get_user_model(), pk=request.user.id)
    recent_friend_photos = []

    for photo in Photo.objects.exclude(published="private").order_by('-date_uploaded')[:4]:
        for follower in photo.user.followers.all():
            if request.user.id == follower.id:
                recent_friend_photos.append(photo)

    photos_to_stream = random.sample(recent_friend_photos, min(len(recent_friend_photos), 4))
    context = {'friends_photos': photos_to_stream, 'user_photos': recent_user_photos}

    return render(request, 'imagr_app/stream.html', context)
