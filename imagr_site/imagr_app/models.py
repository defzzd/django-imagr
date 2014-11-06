from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime

# Create your models here.


# After you have that working, you'll also want to create a customized User class:

#     ImagrUser should be based off of the standard built-in Django User, with the following enhancements:
#         Users should be able to follow other users.
#         Users should be able to see a list of the users the follow and the list of users following them.
#         Users should have a 'date_joined' field and an 'active' field that allows disabling an account.
class ImagrUser(AbstractBaseUser):
    identifier = models.CharField(max_length=40, unique=True, default=None)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="ImagrUser_followers")
    following = models.ManyToManyField("self", symmetrical=False, related_name="ImagrUser_following")
    our_date_joined_field = models.DateField(auto_now_add=True)
    our_is_active_field = models.BooleanField(default=False)
    USERNAME_FIELD = 'identifier'

#     Photo contains an image and meta-data associated with that image
#         Photos are owned by Users
#         Meta-data should include a title and a description.
#             A date_uploaded, date_modified and date_published field.
#             You should also have a 'published' field takes one of three values ('private', 'shared', 'public')
PUBLISHED_CHOICES = (
    ("private", "Private Photo"),
    ("shared",  "Shared Photo"),
    ("public",  "Public Photo")
    )

class Photo(models.Model):
    user = models.ForeignKey(ImagrUser)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=140)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField()
    published = models.CharField(max_length=7,
                                choices=PUBLISHED_CHOICES,
                                default="private")
    # The name for an AWS S3 url is actually an object key.
    # These object keys are sequences of Unicode characters
    # whose UTF-8 encoding is at most 1024 bytes long.
    image_url = models.CharField(max_length=1024, default="Photo Not Found")

#     Album contains Photos and provide meta-data about the collection of photos they contain.
#         Albums are owned by Users
#         Any album can contain many Photos and any Photo may be in more than one Album.
#         Meta-data should include a title and a description. Also a date created, date modified and date published as well as a published field containing the same three options described for Photos
#         Users should be able to designate one contained photo as the 'cover' for the album.
#         The albums created by a user may contain only Photos created by that same user.
class Album(models.Model):
    user = models.ForeignKey(ImagrUser)
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=140)
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    date_published = models.DateField()
    published = models.CharField(max_length=7,
                                choices=PUBLISHED_CHOICES,
                                default="private")
    cover = models.ForeignKey(Photo, related_name='Album_cover')
    photos = models.ManyToManyField(Photo, related_name="Album_photos")



