from django.db import models

# Create your models here.
class Brand(models.Model):
  brand_id = models.AutoField(primary_key=True,)
  brand_name = models.CharField(max_length=30, unique=True)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.brand_name
  
class Category(models.Model):
  category_id = models.AutoField(primary_key=True,)
  category_name = models.CharField(max_length=30, unique=True)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.category_name