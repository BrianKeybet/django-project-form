from django.contrib import admin
from .models import *

admin.site.register(Department)
admin.site.register(Supplier)
admin.site.register(Reason)
admin.site.register(Resolution)
admin.site.register(Material)
admin.site.register(RTSform)
admin.site.register(EmailAddress)

# Register your models here.
