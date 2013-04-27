from django.conf.urls import patterns, include, url
from settings import DEBUG, STATIC_ROOT

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^splash/?$', 'groupjam.views.splash', name='splash'),
    url(r'^/?$', 'groupjam.views.home', name='home'),
    url(r'^home/?$', 'groupjam.views.home', name='home'),
    url(r'^thread/?$', 'groupjam.views.thread', name='thread'),
    url(r'^group/?$', 'groupjam.views.group', name='group'),
    # url(r'^groupjam/', include('groupjam.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': STATIC_ROOT,
        }),
    )