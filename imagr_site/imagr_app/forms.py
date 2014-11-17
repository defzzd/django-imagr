from django.forms import ModelForm
#from django import forms

import models



# PUBLISHED_CHOICES = (
#     ("private", "Private Photo"),
#     ("shared",  "Shared Photo"),
#     ("public",  "Public Photo")
#     )


class CreatePhotoForm(ModelForm):

    class Meta:
        model = models.Photo
        fields = ['title', 'description', 'published', 'image_url']


class CreateAlbumForm(ModelForm):

    class Meta:
        model = models.Album
        fields = ['title', 'description', 'published', 'cover', 'photos']


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

