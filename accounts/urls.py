from django.conf.urls import patterns, include, url
from forms import LoginForm

urlpatterns = patterns('',
    # Examples:
    url(r'register/?$', 'accounts.views.register_start', name='register', kwargs={'template': 'registration/register_email.html'}),
    url(r'register/confirm/?$', 'accounts.views.register_email_confirm', name='register_confirm'),
    url(r'register/person/?$', 'accounts.views.register_person', name='register_person'),
    #url(r'register/picture/?$', 'accounts.views.register_person', name='register_person'),
    url(r'register/organization/?$', 'accounts.views.register_organization', name='register_organization'),
    url(r'edit/organization/?$', 'accounts.views.edit_organization', name='edit_organization'),
    url(r'edit/person/?$', 'accounts.views.edit_person', name='edit_person'),
    
    url(r'login/?$', 'django.contrib.auth.views.login', {'authentication_form': LoginForm}, name='login'),
    url(r'logout/?$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/'}),
    url(r'password_change/?$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'password_change_done/?$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'password_reset/$', 'django.contrib.auth.views.password_reset', name="password_reset"),
    url(r'password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name="password_reset_done"),
    url(r'reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name="password_reset_confirm"),
    url(r'reset/done/$', 'django.contrib.auth.views.password_reset_complete', name="reset_complete")
)
