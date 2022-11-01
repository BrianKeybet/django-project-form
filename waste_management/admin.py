from django.contrib import admin
from .models import waste_delivery_note, Material, checklist, kgrn, goods_issue_note, Department, Resolve, kgrn_item, Reason
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(waste_delivery_note)
admin.site.register(goods_issue_note)
admin.site.register(Material, SimpleHistoryAdmin)
admin.site.register(checklist)
admin.site.register(kgrn)
admin.site.register(Department)
admin.site.register(Resolve)
admin.site.register(Reason)
admin.site.register(kgrn_item)