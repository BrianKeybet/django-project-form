from django.contrib import admin
from .models import waste_delivery_note, Material, checklist

# Register your models here.
admin.site.register(waste_delivery_note)
admin.site.register(Material)
admin.site.register(checklist)