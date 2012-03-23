from django import newforms as forms
from minierp.warehouse.models import Product, Category

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=200)


class CategoryExistForm(CategoryForm):
    def clean_name(self):
        """ Check if the category already exist. """
        try:
            Category.objects.get(name__exact=self.clean_data['name'])
        except Category.DoesNotExist:
            return self.clean_data['name']
        raise forms.ValidationError(u'Category with this name already exists.')


class ProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [('', '----------')] + [
            (c.id, c.name) for c in Category.objects.all()]

    description = forms.CharField(max_length=200)
    detail = forms.CharField(max_length=400)
    category = forms.ChoiceField(choices=())
    cost = forms.IntegerField()
    quantity = forms.IntegerField()


class ProductExistForm(ProductForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

    def clean_description(self):
        """ Check if the product already exist. """
        try:
            Product.objects.get(
                description__exact=self.clean_data['description'])
        except Product.DoesNotExist:
            return self.clean_data['description']
        raise forms.ValidationError(u'Product with this name already exists.')
