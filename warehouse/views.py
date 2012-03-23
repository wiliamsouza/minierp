from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list_detail import object_list
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django import newforms as forms

from minierp.warehouse.models import Category, Product, Requisition
from minierp.warehouse.forms import CategoryForm, ProductForm

@login_required
def index(request):
    return render_to_response(
        'warehouse/index.html',
        context_instance=RequestContext(request)
        )

#@login_required
@permission_required('warehouse.add_requisition')
def requisition(request):
    RequisitionForm = forms.form_for_model(Requisition)
    form = RequisitionForm()
    title = 'Requisition'
    return render_to_response(
        'warehouse/requisition.html',
        {'form': form,
         'title': title},
        context_instance=RequestContext(request)
        )


#@login_required
@permission_required('warehouse.add_product')
def product_bad(request, product_id=0):
    title = 'Add product'
    action = 'add'
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        form = ProductForm(product.__dict__)
        form.fields['category'].initial = '1'
        title = 'Editing product'
        action = 'update'
    else:
        form = ProductForm()
    if request.method == 'POST':
        category = Category.objects.get(pk=request.POST['category'])
        if request.POST['action'] == 'add':
            form = ProductForm(request.POST.copy())
            if form.is_valid():
                new = Product(description=form.clean_data['description'],
                              detail=form.clean_data['detail'],
                              category=category,
                              cost=form.clean_data['cost'],
                              quantity=form.clean_data['quantity'])
                new.save()
        if request.POST['action'] == 'update':
            if form.is_valid():
                for field in ['description', 'detail', 'cost', 'quantity']:
                    setattr(product, field, form.clean_data[field])
                product.category = category
                product.save()
        return HttpResponseRedirect(
            '%s/%i/' % ('/warehouse/product', request.POST['category'])
            )
    return render_to_response(
        'warehouse/product.html',
        {'form': form,
         'title': title,
         'action': action},
        context_instance=RequestContext(request)
        )

#@login_required
@permission_required('warehouse.add_product')
def product(request, product_id=0):
    ProductForm = forms.form_for_model(Product)
    title = 'Add product'
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        ProductForm = forms.form_for_instance(product)
        title = 'Editing product'
    if request.method == 'POST':
        form = ProductForm(request.POST.copy())
        if form.is_valid():
            p = form.save()
            return HttpResponseRedirect('%s/%i/'%('/warehouse/product', p.id))
    else:
        form = ProductForm()
    return render_to_response(
        'warehouse/product.html',
        {'form': form,
         'title': title},
        context_instance=RequestContext(request)
        )

#@login_required
@permission_required('warehouse.add_category')
def category(request, category_id=0):
    CategoryForm = forms.form_for_model(Category)
    title = 'Add category'
    if category_id:
        category = Category.objects.get(pk=category_id)
        CategoryForm = forms.form_for_instance(category)
        title = 'Editing category'
    if request.method == 'POST':
        form = CategoryForm(request.POST.copy())
        if form.is_valid():
            c = form.save()
            return HttpResponseRedirect('%s/%i/'%('/warehouse/category', c.id))
    else:
        form = CategoryForm()
    return render_to_response(
        'warehouse/category.html',
        {'form': form,
         'title': title},
        context_instance=RequestContext(request)
        )

#@login_required
@permission_required('warehouse.view_product')
def products_list(request):
    return object_list(
        request       = request,
        queryset      = Product.objects.order_by('description'),
        template_name = 'warehouse/products_list.html',
        paginate_by   = 50,
        extra_context = {'url': '/warehouse/product/',
                         'noavailable': 'No products are available.'}
        )

#@login_required
@permission_required('warehouse.view_category')
def categories_list(request):
    return object_list(
        request       = request,
        queryset      = Category.objects.order_by('name'),
        template_name = 'warehouse/categories_list.html',
        paginate_by   = 50,
        extra_context = {'url': '/warehouse/category/',
                         'noavailable': 'No categories are available.'}
        )
