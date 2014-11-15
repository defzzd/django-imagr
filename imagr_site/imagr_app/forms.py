from django.forms import ModelForm
from imagr_app.models import Album
from imagr_app.models import Photo


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description']


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'description', 'published', 'photo_data']
