from django.shortcuts import render
from .models import waste_delivery_note
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from datetime import date

# Create your views here.
class waste_delivery_noteCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    today = date.today()
    template_name = 'waste_management/waste_dnote.html'
    success_message = 'Form Submitted Sccessfully!'
    model = waste_delivery_note
    fields = ['item1', 'item_qty1', 'item2', 'item_qty2', 'item3', 'item_qty3', 'item4', 'item_qty4', 'item5', 'item_qty5']