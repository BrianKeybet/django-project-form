from django.shortcuts import redirect, render
from .models import waste_delivery_note
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from datetime import date
from .forms import WasteForm
from . import models
from users.models import Profile
from django.core.mail import EmailMessage
from django.contrib import messages
from decouple  import config
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView

# Create your views here.
class waste_delivery_noteCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'waste_management/waste_dnote.html'
    success_message = 'Form Submitted Successfully!'
    model = waste_delivery_note
    form_class = WasteForm

    def form_valid(self,form):
        form.instance.author = self.request.user #Inserts the author into the new post
        form.instance.department = self.request.user.profile.department

        prev_serial_num = waste_delivery_note.objects.count()
        serial_num = prev_serial_num + 15 #Get next serial number to display in email

        dept = self.request.user.profile.department
        prof = Profile.objects.get(department=f'{dept}',level='2')
        em = prof.email #Gets email account of the HOD from the logged in user's department

        email = EmailMessage(
        subject=f'{form.instance.department} department Waste Delivery Note',
        body=f'Waste Delivery Note number {serial_num} has been submitted by {form.instance.author}.\nKindly log on to the portal to view it.\vIn case of any challenges, feel free to contact IT for further assistance.',
        from_email=config('EMAIL_HOST_USER'),
        # to=[f'{em}'],
        to=[config('BRIAN_EMAIL')],
        cc=[config('BRIAN_EMAIL')],
        reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
        )
        # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
        email.send()
        # messages.success(self.request, 'Form submitted and mail sent!')
        return super().form_valid(form)

class DnotesListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'waste_delivery_notes'
    template_name = 'waste_management/waste_dnotes_list.html'

    def get_queryset(self):
        return models.waste_delivery_note.objects.all()          

class DnoteHODUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/dnote_update.html'
    model = waste_delivery_note
    fields = ['hod_comment']

class DnoteWHUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/dnote_update1.html'
    model = waste_delivery_note
    fields = ['waste_offloader', 'warehouse_hod_comment']