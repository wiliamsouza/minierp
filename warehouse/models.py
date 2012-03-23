from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(maxlength=200, unique=True)

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return('minierp.warehouse.views.category', str(self.id))

    class Meta:
        permissions = (("view_category", "Can view category"),)

    class Admin: pass


class Product(models.Model):
    description = models.CharField(maxlength=200)
    category = models.ForeignKey(Category)
    quantity = models.IntegerField()
    cost = models.FloatField(max_digits=10, decimal_places=2)
    detail = models.TextField(maxlength=400, blank=True)

    def __str__(self):
        return self.description

    def name(self):
        return self.description

    @models.permalink
    def get_absolute_url(self):
        return('minierp.warehouse.views.product', str(self.id))

    class Meta:
        permissions = (('view_product', 'Can view product'),)

    class Admin: pass


class Requisition(models.Model):
    products = models.ManyToManyField(Product)
    created_date = models.DateTimeField(editable=False)
    deliver_date = models.DateTimeField(editable=False)
    requester = models.ForeignKey(User,
                                  related_name='requester',
                                  editable=False)
    delivered_by = models.ForeignKey(User,
                                     related_name='delivered_by',
                                     editable=False,
                                     blank=True)

    def __str__(self):
        return '%s %s' % (self.requester.get_full_name)

    @models.permalink
    def get_absolute_url(self):
        return('minierp.warehouse.views.requisition', str(self.id))

    class Admin: pass
