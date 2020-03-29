from django.db import models

# Create your models here.
class LocationData(models.Model):
    email_address = models.EmailField()
    longitude = models.DecimalField(max_digits=8, decimal_places=3)
    latitutde = models.DecimalField(max_digits=8, decimal_places=3)
    timestamp = models.TextField()
