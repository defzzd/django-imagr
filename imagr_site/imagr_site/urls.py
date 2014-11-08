from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^imagr_app/', include('imagr_app.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
