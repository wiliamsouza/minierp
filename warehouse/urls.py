from django.conf.urls.defaults import *
from minierp.warehouse.views import *
from django.contrib import databrowse

urlpatterns = patterns('',
    (r'^$', index),
    (r'^product/(?P<product_id>\d+)/$', product),
    (r'^product/$', products_list),
    (r'^product/add/$', product),
    (r'^category/(?P<category_id>\d+)/$', category),
    (r'^category/$', categories_list),
    (r'^category/add/$', category),
    (r'^requisition/$', requisition),
    (r'^databrowse/(.*)', databrowse.site.root),
)
