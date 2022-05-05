from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from rts_forms.models import Material

# Create your models here.
class waste_delivery_note(models.Model):
    date_posted = models.DateTimeField(default = timezone.now, verbose_name= "Date")
    department = models.CharField(max_length = 20, blank = True)
    author = models.ForeignKey(User, null = True, on_delete = models.PROTECT)
    items_disposed = models.ForeignKey(Material, on_delete = models.PROTECT, verbose_name = "Material Description")
    material_quantity = models.FloatField(max_length = 40, verbose_name = "Estimated Quantity")

