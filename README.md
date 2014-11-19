#django-imagr
============
[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/CharlesGust/django-imagr?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


This was produced by Charlie Rode, Ben Friedland, and Charles Gust


## Views overview ##

In addition to incorporating the django-registration-redux library
    for user registration, Imagr has eleven custom page views.

    front_page:
        Allows users to sign up and log in.
    home_page:
        Shows logged-in users a list of their albums, with a representative
        image from each album.
    album_page:
        Shows logged-in users a display of photos in a single album and
        allows logged-in users the ability to edit the album's details.
    photo_page:
        Shows logged-in users a single photo along with details about it
        and allows logged-in users the ability to edit the photo's details.
    stream_page:
        Shows users their most recent photos along with recent photos
        uploaded by those they are following.
    add_photo:
        Allows users to add a photo to the site.
    add_album:
        Allows users to add an album to the site and associate it with
        a selection of their photos.
    delete_photo:
        Allows users to delete photos they own.
    delete_album:
        Allows users to delete photos they own without deleting photos.
    follow_page:
        Shows logged-in users a display of users they are following and
        allows them to follow and unfollow users.
    history_page:
        Shows logged-in users a chronologically-ordered list of their photos.


## Commands to set up the database ##

1. Enter PSQL with this command:
sudo -u postgres psql -U postgres postgres

2. From inside the PSQL, type in these commands:
postgres=# CREATE DATABASE imagr;

3. Create the user:
postgres=# CREATE role imagr login password 'imagr';

4. Set the owner to that user:
postgres=# ALTER database imagr OWNER to imagr;

5. Check your work:
postgres=# \l

6. Leave PSQL:
postgres=# \q

6. Migrate the database using Django's manage.py utility:
python manage.py migrate


## Description of the database model ##

Photo contains an image and meta-data associated with that image.

    Photos are owned by Users
    Meta-data includes a title and a description.
        A date_uploaded, date_modified and date_published field.
        They also have a 'published' field that takes one of three values
        ('private', 'shared', 'public')

Album contains Photos and provide meta-data about the collection of
    photos they contain.

    Albums are owned by Users
    Any album can contain many Photos and any Photo may be in
        more than one Album.
    Meta-data includes a title and a description.
        Also a date created, date modified and date published as well
        as a published field containing the same three options described for Photos
    Users are able to designate one contained photo as the 'cover' for
        the album.
    The albums created by a user may contain only Photos created by
        that same user.

ImagrUser is based off of the standard built-in Django User, with the
    following enhancements:

    Users are able to follow other users.
    Users are able to see a list of the users the follow and the
        list of users following them.
    Users have a 'date_joined' field and an 'active' field that allows
        disabling an account.


## References used ##

Just about everywhere:
    docs.djangoproject.com
    The invaluable advice of Dan T. Hable

settings.py:
    stackoverflow.com/questions/21978562

admin.py:
    stackoverflow.com/questions/11754877
    stackoverflow.com/questions/2156114
