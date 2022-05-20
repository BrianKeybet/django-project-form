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
from django.shortcuts import get_object_or_404, redirect, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def rtsforms_render_pdf_view(request, *args, **kwargs):
   pk = kwargs.get('pk')
   dnote = get_object_or_404(waste_delivery_note, pk=pk)

   template_path = 'waste_management/generate_pdf.html'
   context = {'dnote': dnote}
   # Create a Django response object, and specify content_type as pdf
   response = HttpResponse(content_type='application/pdf')

   # to directly download the pdf we need attachment 
   # response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # to view on browser we can remove attachment 
   response['Content-Disposition'] = 'filename="report.pdf"'

   # find the template and render it.
   template = get_template(template_path)
   html = template.render(context)

   # create a pdf
   pisa_status = pisa.CreatePDF(
      html, dest=response)
   # if error then show some funy view
   if pisa_status.err:
      return HttpResponse('We had some errors ' + html + '')
   return response

# Create your views here.
class waste_delivery_noteCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'waste_management/waste_dnote.html'
    success_message = 'Form Submitted Successfully!'
    model = waste_delivery_note
    form_class = WasteForm

    def form_valid(self,form):
        form.instance.form_status = 2 #Increases the form status by 2

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

    def form_valid(self, form):
        form.instance.hod = self.request.user
        if ('elevate' in self.request.POST) and (form.instance.form_status == 2):
            form.instance.form_status += 2

            email = EmailMessage(
            subject=f'{form.instance.department} department Waste Delivery Note',
            body=f'Waste delivery note number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        if ('elevate' in self.request.POST) and (form.instance.form_status == 3):
            form.instance.form_status += 1
            email = EmailMessage(
            subject=f'{form.instance.department} department Waste Delivery Note',
            body=f'Waste delivery note number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 2):
            form.instance.form_status -= 1

            email = EmailMessage(
            subject=f'{form.instance.department} department Waste Delivery Note',
            body=f'Waste delivery note number {form.instance.id} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        if ('demote' in self.request.POST) and (form.instance.form_status == 3):
            form.instance.form_status -= 2

            email = EmailMessage(
            subject=f'{form.instance.department} department Waste Delivery Note',
            body=f'Waste delivery note number {form.instance.id} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

class DnoteWHUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/dnote_update1.html'
    model = waste_delivery_note
    fields = ['waste_offloader', 'warehouse_hod_comment']

    def form_valid(self, form):
        form.instance.warehouse_hod = self.request.user

        if ('elevate' in self.request.POST) and (form.instance.form_status == 4):
            form.instance.form_status += 2

            email = EmailMessage(
            subject=f'{form.instance.department} department Waste Delivery Note',
            body=f'Waste delivery note number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)


        if ('demote' in self.request.POST) and (form.instance.form_status == 4):
            form.instance.form_status -= 1

            email = EmailMessage(
            subject=f'{form.instance.department} department Waste Delivery Note',
            body=f'Waste delivery note number {form.instance.id} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)