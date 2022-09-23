from django.forms import ModelForm
from . import models

class WasteForm(ModelForm):
    class Meta:
        model = models.waste_delivery_note
        fields = ['item1', 'item_qty1', 'item2', 'item_qty2', 'item3', 'item_qty3', 'item4', 'item_qty4',
                 'item5', 'item_qty5', 'item6', 'item_qty6', 'item7', 'item_qty7', 'item8', 'item_qty8', 'supplier', 'waste_loader']

class GoodsIssueNoteForm(ModelForm):
    class Meta:
        
        model = models.goods_issue_note
        fields = ['time_in','time_out','item1', 'item_qty1', 'item2', 'item_qty2', 'item3', 'item_qty3', 'item4', 'item_qty4',
                 'item5', 'item_qty5', 'item6', 'item_qty6', 'item7', 'item_qty7', 'item8', 'item_qty8', 'department_to', 'department_from', 'delivered_by', 'isInternal']

        # def __init__(self,  *args, **kwargs):
        #     self.helper.form_show_labels = False    