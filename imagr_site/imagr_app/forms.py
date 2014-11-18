
from django import forms

import models


# PUBLISHED_CHOICES = (
#     ("private", "Private Photo"),
#     ("shared",  "Shared Photo"),
#     ("public",  "Public Photo")
#     )


class CreatePhotoForm(forms.ModelForm):

    class Meta:
        model = models.Photo
        fields = ['title', 'description', 'published', 'image_url']


class CreateAlbumForm(forms.ModelForm):

    class Meta:
        model = models.Album
        fields = ['title', 'description', 'published', 'cover', 'photos']


# Some non-required fields when editing:
class EditPhotoForm(forms.ModelForm):
    title = forms.CharField(max_length=60, required=False)
    description = forms.CharField(max_length=140, required=False)
    image_url = forms.CharField(max_length=1024, required=False)

    class Meta:
        model = models.Photo
        fields = ['title', 'description', 'published', 'image_url']


class EditAlbumForm(forms.ModelForm):
    title = forms.CharField(max_length=60, required=False)
    description = forms.CharField(max_length=140, required=False)

    # Pandora's box...!
    # cover = forms.ModelChoiceField()
    # photos = forms.ModelMultipleChoiceField()

    class Meta:
        model = models.Album
        fields = ['title', 'description', 'published', 'cover', 'photos']

    # def __init__(self, *args, **kwargs):
    #     super(EditAlbumForm, self).__init__(*args, **kwargs)
    #     self.fields['cover'] = forms.ModelChoiceField(queryset=None)
    #     self.fields['photos'] = forms.ModelMultipleChoiceField(queryset=None)


# class EditPhotoForm(ModelForm):

#     class Meta:
#         model = models.Photo
#         fields = ['title', 'description', 'published', 'image_url']


# class CreatePhotoForm(forms.Form):
#     title = forms.CharField(label='Photo title', max_length=20)
#     description = forms.CharField(label='Photo description', max_length=140)
#     published = forms.ChoiceField(label='Photo publishing', widget=forms.RadioSelect, choices=PUBLISHED_CHOICES)
#     image_url = forms.URLField(label='Image URL', max_length=1024)
#     album = forms.ModelMultipleChoiceField(queryset=models.Album.objects.filter(user=).order_by('-date_uploaded'))


# class CreateAlbumForm:


#     pass

