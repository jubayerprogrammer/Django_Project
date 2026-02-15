from django.db import models

# Create your models here.
class qr_code(models.Model):
    data = models.CharField(max_length=225)
    phon_number = models.CharField(max_length=225)
    