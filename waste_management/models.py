from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from rts_forms.models import Material

# Create your models here.
class waste_delivery_note(models.Model):
    date_posted = models.DateTimeField(default = timezone.now, verbose_name= "Date")
    department = models.CharField(max_length = 20, blank = True)
    author = models.ForeignKey(User, null = True, on_delete = models.PROTECT)
    item1 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material1', verbose_name = "Material Description")
    item_qty1 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item2 = models.ForeignKey(Material, on_delete = models.PROTECT,null = True, blank = True, related_name = 'material2', verbose_name = "Material Description")
    item_qty2 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item3 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material3', verbose_name = "Material Description")
    item_qty3 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item4 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material4', verbose_name = "Material Description")
    item_qty4 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item5 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material5', verbose_name = "Material Description")
    item_qty5 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")

