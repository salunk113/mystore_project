from django.db import models

# Create your models here.
class Carts(models.Model):
    product=models.CharField(max_length=12)
    user=models.CharField(max_length=120)
    date=models.DateField(auto_now_add=True)
    status=models.CharField(max_length=120)

# samsung,ram,incart
#