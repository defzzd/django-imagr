from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from models import ImagrUser, Photo, Album


def front_page(request):
    return render(request, 'imagr_app/front_page.html')


    #if request.user.is_authenticated():
        # This may need to call HttpResponseRequest() instead of render()
    #    return render(request, 'imagr_app/home_page.html')
    #else:
    #    return render(request, 'imagr_app/front_page.html')


def album_page(request, album_id):
    album = Album.objects.get(id=album_id)
    photos = album.photos.all()
    context = {'photos': photos}
    return render(request, 'imagr_app/album.html', context)


def photo_page(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    context = {'photo': photo}
    return render(request, 'imagr_app/photo.html', context)


def stream(request):
    return HttpResponse("Stream")
