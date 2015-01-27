from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from main.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'main.views.mainpage', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^logout/$', 'main.views.LogoutRequest'),
    url(r'^login/$', 'main.views.LoginRequest'),
    url(r'^register/$', 'main.views.PosterRegistration'),
    url(r'^profile/$', 'main.views.Profile'),
    url(r'^search/', include('haystack.urls')),
    url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect' : '/resetpassword/passwordsent/'}),
    url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect' : '/reset/done/'}),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^(?P<category_slug>[^\.]+)/$', 'main.views.categorypage', name="view_category"),
    url(r'^(?P<category_slug>[^\.]+)/(?P<post_slug>[^\.]+).html', 'main.views.postpage', name="view_post"),
    url(r'^tag/(?P<tag_slug>[^\.]+)', 'main.views.tagpage', name="view_tag"),
)


if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    (r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog')
) + urlpatterns