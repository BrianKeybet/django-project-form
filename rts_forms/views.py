from xml.etree.ElementTree import Comment
from django import views
from django.http import response
from django.shortcuts import render, HttpResponse
from django.views import generic
from django.views.generic import DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from . import models
from .models import RTSform
from users.models import Profile
from .forms import RTSForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from decouple  import config
from django.contrib import messages

from django.template.loader import get_template
from xhtml2pdf import pisa 

def home(request):
    return render(request, 'forms/home.html', {'title':'About'})

def rtsforms_render_pdf_view(request, *args, **kwargs):
   pk = kwargs.get('pk')
   rtsform = get_object_or_404(RTSform, pk=pk)

   template_path = 'forms/generate_pdf.html'
   context = {'rtsform': rtsform}
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


class RTSForm(LoginRequiredMixin, SuccessMessageMixin,  generic.CreateView):
    template_name = 'forms/rtsform.html'
    success_message = 'Submitted successfully!'
    form_class = RTSForm

    def form_valid(self,form):
        form.instance.author = self.request.user #Inserts the author into the new post
        form.instance.department = self.request.user.profile.department

        prev_serial_num = RTSform.objects.count()
        serial_num = prev_serial_num + 1 #Get next serial number to display in email

        #dept = self.request.user.profile.department
        #prof = Profile.objects.get(department=f'{dept}',level='2')
        #em = prof.email #Gets email account of the HOD from the logged in user's department

        email = EmailMessage(
        subject=f'{form.instance.department} department R.T.S form',
        body=f'R.T.S form number {serial_num} has been submitted by {form.instance.author}, kindly log on to the portal on http://10.10.1.195:8000/forms/home/ to view it.  \n Supplier name: {form.instance.supplier.name}.\n Product name: {form.instance.material_description.name}. \n Nature of complaint: {form.instance.quality_issue}.\nIn case of any challenges, feel free to contact IT for further assistance.',
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

class FormsView(generic.ListView):
    context_object_name = 'rtsforms'
    template_name = 'forms/rtsforms.html'
    paginate_by: int = 2

    def get_queryset(self):
        return models.RTSform.objects.all()  

class FormsDetailView(DetailView):
    template_name = 'forms/rtsform_detail.html'
    model = RTSform  

class FormsHODUpdateView(UpdateView):
    template_name = 'forms/rtsform_update.html'
    model = RTSform
    fields = ['hod_comment','image','department_internal']

    def form_valid(self, form):
        dept = form.instance.department_internal
        profs = Profile.objects.filter(department=f'{dept}',level='2')
        #em = prof.values_list('email', flat=True) #Gets email account of the HOD from the logged in user's department

        if ('elevate' in self.request.POST) and (form.instance.form_status == 0):
            form.instance.form_status += 2

            for prof in profs:
                email = EmailMessage(
                subject=f'{form.instance.department} department R.T.S form',
                body=f'R.T.S form number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}, kindly log on to http://10.10.1.195:8000/forms/home/ to view it.  In case of any challenges feel free to contact IT for further assistance.',
                from_email=config('EMAIL_HOST_USER'),
                to=[prof.user.email, config('BRIAN_EMAIL')],
                cc=[config('BRIAN_EMAIL')],
                reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
                )
                # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
                email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        if ('elevate' in self.request.POST) and (form.instance.form_status == 1):
            form.instance.form_status += 1

            email = EmailMessage(
            subject=f'{form.instance.department} department R.T.S form',
            body=f'R.T.S form number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}, kindly log on to  http://10.10.1.195:8000/forms/home/  to view it.  In case of any challenges feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 0):
            form.instance.form_status -= 1

            email = EmailMessage(
            subject=f'{form.instance.department} department R.T.S form',
            body=f'R.T.S form number {form.instance.id} submitted by {form.instance.author} has been rejected by {self.request.user}, kindly log on to  http://10.10.1.195:8000/forms/home/  to view it.  In case of any challenges feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        if ('demote' in self.request.POST) and (form.instance.form_status == 1):
            form.instance.form_status -= 2

            email = EmailMessage(
            subject=f'{form.instance.department} department R.T.S form',
            body=f'R.T.S form number {form.instance.id} submitted by {form.instance.author} has been rejected by {self.request.user}, kindly log on to  http://10.10.1.195:8000/forms/home/  to view it.  In case of any challenges feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

class FormsQAOUpdateView(UpdateView):
    template_name = 'forms/rtsform_update1.html'
    model = RTSform
    fields = ['qao_comment']

    def form_valid(self, form):
        if ('elevate' in self.request.POST) and (form.instance.form_status == 2):
            form.instance.form_status += 2

            email = EmailMessage(
            subject=f'{form.instance.department} department R.T.S form',
            body=f'R.T.S form number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}, kindly log on to  http://10.10.1.195:8000/forms/home/  to view it.  In case of any challenges feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')

            return super().form_valid(form)

        if ('elevate' in self.request.POST) and (form.instance.form_status == 3):
            form.instance.form_status += 1

            email = EmailMessage(
            subject=f'{form.instance.department} department R.T.S form',
            body=f'R.T.S form number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}, kindly log on to  http://10.10.1.195:8000/forms/home/  to view it.  In case of any challenges feel free to contact IT for further assistance.',
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
            subject=f'{form.instance.department} department R.T.S form',
            body=f'R.T.S form number {form.instance.id} submitted by {form.instance.author} has been rejected by {self.request.user}, kindly log on to  http://10.10.1.195:8000/forms/home/  to view it.  In case of any challenges feel free to contact IT for further assistance.',
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
            subject=f'{form.instance.department} department R.T.S form',
            body=f'R.T.S form number {form.instance.id} submitted by {form.instance.author} has been rejected by {self.request.user}, kindly log on to  http://10.10.1.195:8000/forms/home/  to view it.  In case of any challenges feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')

            return super().form_valid(form)

    def get_absolute_url(self):
        return reverse_lazy('rtsforms')        

class FormsFMUpdateView(UpdateView):
    template_name = 'forms/rtsform_update2.html'
    model = RTSform
    fields = ['resolution']

    def form_valid(self, form):
        if 'elevate' in self.request.POST:
            form.instance.form_status += 2

            email = EmailMessage(
            subject=f'{form.instance.department} department R.T.S form',
            body=f'R.T.S form number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}, kindly log on to  http://10.10.1.195:8000/forms/home/  to view it.  In case of any challenges feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')

            return super().form_valid(form)

        if 'demote' in self.request.POST:
            form.instance.form_status -= 1

            email = EmailMessage(
            subject=f'{form.instance.department} department R.T.S form',
            body=f'R.T.S form number {form.instance.id} submitted by {form.instance.author} has been rejected by {self.request.user}, kindly log on to  http://10.10.1.195:8000/forms/home/  to view it.  In case of any challenges feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')

            return super().form_valid(form)

    def get_absolute_url(self):
        return reverse_lazy('rtsform') 

class FormsPrintView(DetailView):
    template_name = 'forms/rtsform_print.html'
    model = RTSform          

#I used the below functions to change form status using a link on the templates, no longer in use
def elevate_form_status(request, pk):
    rtsform =  get_object_or_404(RTSform, pk=pk)
    rtsform.elevate_status() 
    rtsform.save()
    return redirect('rtsforms')

def demote_form_status(request, pk):
    rtsform =  get_object_or_404(RTSform, pk=pk)
    rtsform.demote_status() 
    rtsform.save()
    return redirect('rtsforms')

def get_material_image(request, pk):
    rtsform = get_object_or_404(RTSform, pk=pk)
    return render(request, 'forms/rtsform_photo.html', {'form': rtsform })

