from django.shortcuts import render
from .models import waste_delivery_note
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic

# Create your views here.
class waste_delivery_noteCreateView(SuccessMessageMixin, generic.CreateView):
    template_name = 'waste_management/waste_dnote.html'
    success_message = 'Form Submitted Sccessfully!'
    model = waste_delivery_note
    fields = ['items_disposed', 'material_quantity']