from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django import newforms as forms

from minierp.purchase.models import Supplier, Order, Item
from minierp.warehouse.models import Product


@login_required
def index(request):
    return render_to_response(
        'purchase/index.html',
        context_instance=RequestContext(request)
        )

def item(request, supplier_id, order_id):
    ItemForm = forms.form_for_model(Item)
    title = 'Add item'
    supplier = Supplier.objects.get(pk=supplier_id)
    form = ItemForm()
    form.fields['product'].choices = [('', '----------')] + [
        (p['id'], p['description']) for p in supplier.products.values()]
    if request.method == 'POST':
        form = ItemForm(request.POST.copy())
        if form.is_valid():
            order = Order.objects.get(pk=order_id)
            i = Item(product=form.clean_data['product'],
                     quantity=form.clean_data['quantity'],
                     order=order)
            i.save()
            return HttpResponseRedirect('%s/%i/'%('/purchase/order', order.id))
    return render_to_response(
        'purchase/item.html',
        {'form': form,
         'order_id': order_id,
         'supplier_id': supplier_id,
         'title': title},
        context_instance=RequestContext(request)
        )

def order(request, order_id=0):
    OrderForm = forms.form_for_model(Order)
#    supplier_id = 0
    order = None
    items = None
    title = 'Add order'
    if order_id:
        order = get_object_or_404(Order, pk=order_id)
        items = order.item_set.select_related()
        OrderForm = forms.form_for_instance(order)
#        supplier_id = order.supplier.id
        title = 'Editing order'
    if request.method == 'POST':
        form = OrderForm(request.POST.copy())
        if form.is_valid():
            o = form.save()
            return HttpResponseRedirect('%s/%i/'%('/purchase/order', o.id))
    else:
        form = OrderForm()
    return render_to_response(
        'purchase/order.html',
        {'form': form,
         'order': order,
         'items': items,
         'title': title},
        context_instance=RequestContext(request)
        )

#@login_required
#@permission_required('purchase.add_supplier')
def supplier(request, supplier_id=0):
    SupplierForm = forms.form_for_model(Supplier)
    title = 'Add supplier'
    if supplier_id:
        supplier = Supplier.objects.get(pk=supplier_id)
        SupplierForm = forms.form_for_instance(supplier)
        title = 'Editing supplier'
    if request.method == 'POST':
        form = SupplierForm(request.POST.copy())
        if form.is_valid():
            s = form.save()
            return HttpResponseRedirect('%s/%i/'%('/purchase/supplier', s.id))
    else:
        form = SupplierForm()
    return render_to_response(
        'purchase/supplier.html',
        {'form': form,
         'title': title},
        context_instance=RequestContext(request)
        )

#@permission_required('purchase.view_supplier')
def orders_list(request):
    return object_list(
        request       = request,
        queryset      = Order.objects.order_by('opendate'),
        template_name = 'purchase/orders_list.html',
        paginate_by   = 50,
        extra_context = {'url': '/purchase/order/',
                         'noavailable': 'No orders are available.'}
        )

#@permission_required('purchase.view_supplier')
def suppliers_list(request):
    return object_list(
        request       = request,
        queryset      = Supplier.objects.order_by('name'),
        template_name = 'purchase/suppliers_list.html',
        paginate_by   = 50,
        extra_context = {'url': '/purchase/supplier/',
                         'noavailable': 'No suppliers are available.'}
        )
