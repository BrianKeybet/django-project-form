from tkinter import Widget
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
        fields = ['time_in','time_out','item1', 'item_qty1','item_qty1_wh',  'item2', 'item_qty2','item_qty2_wh', 'item3', 'item_qty3',
        'item_qty3_wh',  'item4', 'item_qty4','item_qty4_wh', 'item5', 'item_qty5','item_qty5_wh',  'item6', 'item_qty6', 'item_qty6_wh',
         'item7', 'item_qty7','item_qty7_wh',  'item8', 'item_qty8','item_qty8_wh',  'department_to', 'department_from', 'delivered_by', 'isinternal']

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time_in'].widget.attrs.update({'placeholder': 'HH:MM'})
        self.fields['time_out'].widget.attrs.update({'placeholder': 'HH:MM'})

class KGRNForm(ModelForm):
    class Meta:
        model = models.kgrn_item
        fields = ['item1', 'item_qty1','reason1', 'item2', 'item_qty2','reason2', 'item3', 'item_qty3','reason3', 'item4', 'item_qty4','reason4',
                 'item5', 'item_qty5','reason5', 'item6', 'item_qty6','reason6', 'item7', 'item_qty7','reason7', 'item8', 'item_qty8','reason8', 
                 'supplier', 'waste_loader','collected_by', 'id_number', 'vehicle_no']

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['collected_by'].widget.attrs.update({'placeholder': 'NAME'})
        self.fields['id_number'].widget.attrs.update({'placeholder': 'ID NUMBER'})
        self.fields['vehicle_no'].widget.attrs.update({'placeholder': 'VEHICLE NUMBER'})