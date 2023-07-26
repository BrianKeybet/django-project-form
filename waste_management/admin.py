from django.contrib import admin
from .models import waste_delivery_note, Material, Checklist, kgrn, GoodsIssueNote, Department, Resolve, kgrn_item, Reason, Customer
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
admin.site.register(waste_delivery_note)
admin.site.register(GoodsIssueNote)
admin.site.register(Material, SimpleHistoryAdmin)
admin.site.register(Checklist)
admin.site.register(kgrn)
admin.site.register(Department)
admin.site.register(Resolve)
admin.site.register(Reason)
admin.site.register(kgrn_item)
admin.site.register(Customer)