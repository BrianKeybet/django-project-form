from django.contrib import admin
from .models import Department, Material, Reason, Speaker, Track, BPinspectionform, RTSform, Supplier, Resolution

admin.site.register(Speaker)
admin.site.register(Track)
admin.site.register(Department)
admin.site.register(Supplier)
admin.site.register(Reason)
admin.site.register(Resolution)
admin.site.register(Material)
admin.site.register(BPinspectionform)
admin.site.register(RTSform)

# Register your models here.
