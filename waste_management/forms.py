from django.forms import ModelForm
from . import models

class WasteForm(ModelForm):
    class Meta:
        model = models.waste_delivery_note
        fields = ['item1', 'item_qty1', 'item2', 'item_qty2', 'item3', 'item_qty3', 'item4', 'item_qty4', 'item5', 'item_qty5']