from django.conf.urls import patterns, include, url
from settings import DEBUG, STATIC_ROOT

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url(r'^accounts/', include('accounts.urls')),
    
    # Examples:
    url(r'^splash/?$', 'groupjam.views.splash', name='splash'),
    url(r'^/?$', 'groupjam.views.feed', name='feed'),
    url(r'^feed/?$', 'groupjam.views.feed', name='feed'),
    url(r'^calendar/?$', 'groupjam.views.calendar', name='calendar'),
    url(r'^old/?$', 'groupjam.views.old', name='old'),
    url(r'^box/?$', 'groupjam.views.box', name='box'),
    url(r'^pictures/?$', 'groupjam.views.pictures', name='pictures'),
    url(r'^settings/?$', 'groupjam.views.settings', name='settings'),
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