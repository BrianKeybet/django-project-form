from django.contrib import admin
from .models import Department, Material, Reason, RTSform, Supplier, Resolution

admin.site.register(Department)
admin.site.register(Supplier)
admin.site.register(Reason)
admin.site.register(Resolution)
admin.site.register(Material)
admin.site.register(RTSform)

# Register your models here.
