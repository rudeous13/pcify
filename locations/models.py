from django.db import models

class Pincode(models.Model):
    pincode_id = models.AutoField(primary_key=True)
    pincode = models.IntegerField()
    area_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30, default="Ahmedabad")

    def __str__(self):
        return f"{self.area_name} ({self.pincode})"
    
class Address(models.Model):
    address_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        null=True,
        related_name="addresses"
    )

    pincode = models.ForeignKey(
        Pincode,
        on_delete=models.CASCADE
    )

    address = models.CharField(max_length=300)

    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.address