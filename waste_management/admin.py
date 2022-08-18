from django.contrib import admin
from .models import waste_delivery_note, Material, checklist, kgrn, goods_issue_note

# Register your models here.
admin.site.register(waste_delivery_note)
admin.site.register(goods_issue_note)
admin.site.register(Material)
admin.site.register(checklist)
admin.site.register(kgrn)