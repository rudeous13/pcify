from django.db import models
# from django.utils import timezone
# from locations.models import *

# # Create your models here.
# class Brand(models.Model):
#   brand_id = models.AutoField(primary_key=True,)
#   brand_name = models.CharField(max_length=30, unique=True)
#   is_active = models.BooleanField(default=True)

#   def __str__(self):
#     return self.brand_name
  
# class Category(models.Model):
#   category_id = models.AutoField(primary_key=True,)
#   category_name = models.CharField(max_length=30, unique=True)
#   is_active = models.BooleanField(default=True)

#   def __str__(self):
#     return self.category_name
  
# class Suppliers(models.Model):
#     supplier_id = models.AutoField(primary_key=True,)
#     supplier_name = models.CharField(max_length=150,)
#     company_name = models.CharField(max_length=150)
#     phone_number = models.BigIntegerField()
#     email = models.CharField(max_length=50, unique=True,)
#     gst_number = models.CharField(max_length=20, unique=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

# class SupplierAddress(AbstractEntityAddress):
#   supplier_address_id = models.AutoField(primary_key=True)
#   supplier = models.ForeignKey('Suppliers', on_delete=models.CASCADE)

#   class Meta:
#     unique_together = ('supplier', 'address')