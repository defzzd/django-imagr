from django.conf.urls import patterns, url

from imagr_app import views


urlpatterns = patterns('',
    url(r'^$', views.front_page, name='front_page'),
    '''
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
    '''
)
