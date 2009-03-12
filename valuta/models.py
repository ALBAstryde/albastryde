from django.db import models

# Create your models here.
class USD(models.Model):
	fecha=models.DateField(primary_key=True)
	cordobas=models.DecimalField(max_digits=12,decimal_places=10)

class Euro(models.Model):
	fecha=models.DateField(primary_key=True)
	cordobas=models.DecimalField(max_digits=12,decimal_places=10)
