from django.contrib.auth import views as authviews
from django.conf.urls.defaults import *
from django.views.static import serve
from django.conf import settings

from minierp.views import index

urlpatterns = patterns('',
    (r'^$', index),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^purchase/', include('minierp.purchase.urls')),
    (r'^warehouse/', include('minierp.warehouse.urls')),
    (r'^accounts/logout/$', authviews.logout, {'next_page' : "/"}),
    (r'^accounts/login/$', authviews.login)
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', serve,
         {'document_root' : settings.MEDIA_ROOT}
         )
    )
