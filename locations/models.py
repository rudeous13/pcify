from django.db import models

# # Create your models here.
# class State(models.Model):
#   state_id = models.AutoField(primary_key=True)
#   state_name = models.CharField(max_length=100, unique=True)

#   def __str__(self):
#     return self.state_name

# class City(models.Model):
#   city_id = models.AutoField(primary_key=True)
#   city_name = models.CharField(max_length=100)
#   state = models.ForeignKey(State, on_delete=models.RESTRICT)

#   class Meta: 
#     unique_together = ('city_name', 'state')

#   def __str__(self):
#     return f"{self.city_name}, {self.state.state_name}"
  
# class Pincode(models.Model):
#   pincode_id = models.AutoField(primary_key=True)
#   pincode = models.CharField(max_length=15, unique=True)
#   city = models.ForeignKey(City, on_delete=models.RESTRICT)
#   region_name = models.CharField(max_length=100, blank=True, null=True)

#   def __str__(self):
#     return self.pincode
  
# class Address(models.Model):
#   address_id = models.AutoField(primary_key=True)
#   street = models.CharField(max_length=255)
#   pincode = models.ForeignKey(Pincode, on_delete=models.RESTRICT)
#   is_active = models.BooleanField(default=True)
#   created_at = models.DateTimeField(auto_now_add= True)
#   updated_at = models.DateTimeField(auto_now=True)

#   def __str__(self):
#     return f"{self.street} {self.pincode.pincode}"
  
# class AddressType(models.Model):
#   address_type_id = models.AutoField(primary_key=True)
#   address_type = models.CharField(max_length=50, unique= True)

#   def __str__(self):
#     return self.address_type
  
# class AbstractEntityAddress(models.Model):
#   """ Blueprint for connecting entities (Customer, Staff, Supplier) to an Address. """
#   address = models.ForeignKey('locations.Address', on_delete=models.RESTRICT)
#   address_type = models.ForeignKey('locations.AddressType', on_delete=models.RESTRICT)
#   is_primary = models.BooleanField(default=False)
#   created_at = models.DateTimeField(auto_now_add=True)
#   updated_at = models.DateTimeField(auto_now=True)

#   class Meta: 
#     abstract = True