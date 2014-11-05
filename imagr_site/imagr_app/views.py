from django.shortcuts import render

# Create your views here.


from django.views import generic




def front_page(request):

    return render(request, 'imagr_app/front_page.html')



'''
A "front page" that shows anonymous users something nice to
    encourage them to sign up (don't worry that we lack a means for
    them to sign up yet.  We'll add that soon).
A "home page" that shows logged-in users a list of their albums, with
    a representative image from each album
An "album page" that shows logged-in users a display of photos in
    a single album
A "photo page" that shows logged-in users a single photo along with
    details about it.
A "stream" page that shows users their most recent photos along
    with recent photos uploaded by friends or those they are following.
'''