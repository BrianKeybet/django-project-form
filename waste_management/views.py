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
    fields = ['items_disposed', 'material_quantity']