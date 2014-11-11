from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import get_object_or_404
from models import ImagrUser, Photo, Album
from django.contrib.auth.decorators import login_required


def front_page(request):
    if request.user.is_authenticated():
        # This may need to call HttpResponseRequest() instead of render()
        return home_page(request)
    else:
        return HttpResponseRedirect('accounts/login/')
        #return HttpResponseRedirect(request, 'imagr_app/front_page.html')


@login_required
def home_page(request):
    current_user = get_object_or_404(ImagrUser, pk=request.user.id)
    user_albums = Album.objects.filter(user=current_user.id)
    context = {'current_user': current_user, 'user_albums': user_albums}
    return render(request, 'imagr_app/home_page.html', context)


@login_required
def album_page(request, album_id):
    album = Album.objects.get(id=album_id)
    photos = album.photos.all()
    context = {'album': album, 'photos': photos}
    return render(request, 'imagr_app/album.html', context)


@login_required
def photo_page(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    context = {'photo': photo}
    return render(request, 'imagr_app/photo.html', context)


@login_required
def stream(request):
    recent_user_photos = Photo.objects.filter(user=request.user.id).order_by('-date_uploaded')[:4]
    return render(request, 'imagr_app/stream.html', {'recent_user_photos': recent_user_photos})

