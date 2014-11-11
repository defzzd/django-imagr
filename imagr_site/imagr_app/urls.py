from django.conf.urls import patterns, url

from imagr_app import views


urlpatterns = patterns('',
    url(r'^$', views.front_page, name='front_page'),
    url(r'^$', views.home_page, name='home_page'),
    url(r'^album/(?P<album_id>\d+)/$', views.album_page, name='album_page'),
    url(r'^album/(?P<album_id>\d+)/photo/(?P<photo_id>\d+)/$', views.photo_page, name='photo_page'),
    url(r'^stream/$', views.stream_page, name="stream_page")

    # url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
)

# url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
# url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
# url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
