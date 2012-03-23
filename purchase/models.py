from django.db import models

from minierp.warehouse.models import Product


class Order(models.Model):
    supplier = models.ForeignKey('Supplier')
    opendate = models.DateField(auto_now_add=True)
    payment_method = models.ForeignKey('PaymentMethod')
    installment = models.IntegerField()
    receival_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.supplier.name

    def name(self):
        return self.supplier.name

    @models.permalink
    def get_absolute_url(self):
        return('minierp.purchase.views.order', str(self.id))

    class Meta:
        permissions = (('view_order', 'Can view order'),)

    class Admin: pass


class Item(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, editable=False)

    def __str__(self):
        return self.product.description

    def multiply(self):
        return self.product.cost * self.quantity

    class Admin: pass


class PaymentMethod(models.Model):
    method = models.CharField(maxlength=200)

    def __str__(self):
        return self.method

    class Admin: pass


class Supplier(models.Model):
    # Identification
    name = models.CharField(maxlength=200)
    phone = models.CharField(maxlength=15)
    fax = models.CharField(maxlength=15, blank=True)
    email = models.EmailField()
    # Main Address
    street = models.CharField(maxlength=200)
    number = models.IntegerField()
    postal_code = models.CharField(maxlength=15)
    complement = models.CharField(maxlength=200, blank=True)
    district = models.CharField(maxlength=200)
    city = models.CharField(maxlength=200)
    state = models.CharField(maxlength=200)
    country = models.ForeignKey('Country')
    # Company Data
    fancy_name = models.CharField(maxlength=200)
    cnpj = models.CharField(maxlength=200)
    state_registry = models.CharField(maxlength=200)
    # General Details
    status = models.ForeignKey('Status')
    products = models.ManyToManyField(Product)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Admin: pass


class Contact(models.Model):
    name = models.CharField(maxlength=200)
    phone = models.CharField(maxlength=15)    
    email = models.EmailField(blank=True)
    supplier = models.ForeignKey(Supplier)

    def __str__(self):
        return self.name

    class Admin: pass


class Status(models.Model):
    status = models.CharField(maxlength=20)

    def __str__(self):
        return self.status

    class Admin: pass


class Country(models.Model):
    country = models.CharField(maxlength=50)

    def __str__(self):
        return self.country

    class Admin: pass
