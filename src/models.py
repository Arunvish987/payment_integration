from django.db import models

# Create your models here.

class Coffee(models.Model):
    name = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
