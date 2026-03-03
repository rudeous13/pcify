from django.db import models
from django.utils import timezone
# Create your models here.

# Role class for user role 
class Role(models.Model):
  role_id = models.AutoField(primary_key=True,)
  role = models.CharField(max_length=50)

# User class for store user data basic (Custmoter and Employeee)
class User(models.Model):
  user_id = models.AutoField(primary_key=True,)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  email = models.CharField(max_length=50, unique=True,)
  phone = models.BigIntegerField(unique=True)
  password = models.CharField(max_length=16, unique=True)
  role = models.ForeignKey(Role, on_delete= models.CASCADE)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)

class Customer(models.Model):
  customer_id = models.AutoField(primary_key=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)
  
class Staff(models.Model):
  staff_id = models.AutoField(primary_key=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)
  