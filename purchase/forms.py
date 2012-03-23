from django import newforms as forms
from minierp.purchase.models import Supplier, Status, Country

class SupplierForm(froms.Form):
    """ Supplier form """
    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        self.fields['country'].choices = [('', '----------')] + [
            (c.id, c.name) for c in Country.objects.all()]
        self.fields['status'].choices = [('', '----------')] + [
            (s.id, s.name) for c in Status.objects.all()]

    name = froms.CharField(maxlength=200)
    phone = froms.CharField(maxlength=15)
    fax = froms.CharField(maxlength=15)
    email = forms.EmailField()
    street = forms.CharField(maxlength=200)
    number = forms.IntegerField()
    postal_code = forms.CharField(maxlength=15)
    complement = forms.CharField(maxlength=200)
    district = forms.CharField(maxlength=200)
    city = forms.CharField(maxlength=200)
    state = forms.CharField(maxlength=200)
    country = forms.ChoiceField(choices=())
    fancy_name = forms.CharField(maxlength=200)
    cnpj = forms.CharField(maxlength=200)
    state_registry = forms.CharField(maxlength=200)
    status = forms.ChoiceField(choices=())
    notes = forms.TextField()

class SupplierExistForm(SupplierForm):
    """ Supplier form that check if supplier with this name already exists. """

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        """ Check if the supplier already exist. """
        try:
            Supplier.objects.get(name__exact=self.clean_data['name'])
        except Category.DoesNotExist:
            return self.clean_data['name']
        raise forms.ValidationError(u'Supplier with this name already exists.')
