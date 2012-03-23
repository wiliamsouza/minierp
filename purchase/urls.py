from django.conf.urls.defaults import *
from minierp.purchase.views import *
from django.contrib import databrowse

urlpatterns = patterns('',
    (r'^$', index),
    (r'^order/(?P<order_id>\d+)/$', order),
    (r'^order/$', orders_list),
    (r'^order/add/$', order),
    (r'^item/add/supplier/(?P<supplier_id>\d+)/order/(?P<order_id>\d+)/$',
     item),
#    (r'^item/(?P<item_id>\d+)/delete/$', delete_item),
    (r'^supplier/(?P<supplier_id>\d+)/$', supplier),
    (r'^supplier/$', suppliers_list),
    (r'^supplier/add/$', supplier),
    (r'^databrowse/(.*)', databrowse.site.root),
)
