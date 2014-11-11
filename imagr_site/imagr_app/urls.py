from django.conf.urls import patterns, url

from imagr_app import views


urlpatterns = patterns('',
    url(r'^$', views.front_page, name='front_page'),

    # Alternate root page here, perhaps?
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'imagr_app/login.html'}),
    url(r'^album/(?P<album_id>\d+)$', views.album_page, name='album_page'),
    url(r'^album/(?P<album_id>\d+)/photo/(?P<photo_id>\d+)$', views.photo_page, name='photo_page'),
    url(r'^stream$', views.stream, name='stream')

)
