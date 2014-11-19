from django.conf.urls import patterns, url

from imagr_app import views


urlpatterns = patterns('',
    url(r'^$', views.front_page, name='front_page'),
    url(r'^$', views.home_page, name='home_page'),
    url(r'^album/(?P<album_id>\d+)/$', views.album_page, name='album_page'),
    url(r'^photo/(?P<photo_id>\d+)/$', views.photo_page, name='photo_page'),
    url(r'^stream/$', views.stream_page, name='stream_page'),
    url(r'^add_photo/$', views.add_photo, name='add_photo'),
    url(r'^add_album/$', views.add_album, name='add_album'),
    url(r'^delete_photo/(?P<photo_id>\d+)/$', views.delete_photo, name='delete_photo'),
    url(r'^delete_album/(?P<album_id>\d+)/$', views.delete_album, name='delete_album'),
    url(r'^follow/$', views.follow_page, name='follow_page'),
    url(r'^history/$', views.history_page, name='history_page'),

    # url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
)

# url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
# url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
# url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
