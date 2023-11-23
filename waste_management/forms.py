from django.forms import ModelForm
from . import models

class WasteForm(ModelForm):
    class Meta:
        model = models.waste_delivery_note
        fields = ['item1', 'item_qty1', 'item2', 'item_qty2', 'item3', 'item_qty3', 'item4', 'item_qty4',
                 'item5', 'item_qty5', 'item6', 'item_qty6', 'item7', 'item_qty7', 'item8', 'item_qty8', 'supplier', 'waste_loader']

class GoodsIssueNoteForm(ModelForm):
    class Meta:
        
        model = models.GoodsIssueNote
        fields = ['time_in','time_out','material_1', 'material_quantity_1','warehouse_weight_1',  'material_2', 'material_quantity_2','warehouse_weight_2', 'material_3', 'material_quantity_3', 'warehouse_weight_3',
        'material_4', 'material_quantity_4','warehouse_weight_4', 'material_5', 'material_quantity_5','warehouse_weight_5',  'material_6', 'material_quantity_6', 'warehouse_weight_6',
         'material_7', 'material_quantity_7','warehouse_weight_7',  'material_8', 'material_quantity_8','warehouse_weight_8', 'material_9', 'material_quantity_9','warehouse_weight_9',
         'material_10', 'material_quantity_10','warehouse_weight_10','material_11', 'material_quantity_11','warehouse_weight_11','material_12', 'material_quantity_12','warehouse_weight_12',
         'material_13', 'material_quantity_13','warehouse_weight_13','material_14', 'material_quantity_14','warehouse_weight_14','material_15', 'material_quantity_15','warehouse_weight_15',
        'department_to', 'department_from', 'delivered_by', 'isinternal']

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