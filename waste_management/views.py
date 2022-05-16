from django.shortcuts import render
from .models import waste_delivery_note
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from datetime import date
from .forms import WasteForm
from users.models import Profile
from django.core.mail import EmailMessage
from django.contrib import messages
from decouple  import config

# Create your views here.
class waste_delivery_noteCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    today = date.today()
    template_name = 'waste_management/waste_dnote.html'
    success_message = 'Form Submitted Sccessfully!'
    form_class = WasteForm
    # fields = ['item1', 'item_qty1', 'item2', 'item_qty2', 'item3', 'item_qty3', 'item4', 'item_qty4',
    #           'item5', 'item_qty5', 'item6', 'item_qty6', 'item7', 'item_qty7', 'item8', 'item_qty8']

    def post(self, request, form, *args, **kwargs):
        form = WasteForm(request.POST)
        if form.is_valid():
            if 'elevate' in self.request.POST:
                form.instance.author = self.request.user #Inserts the author into the new post
                form.instance.department = self.request.user.profile.department

                prev_serial_num = WasteForm.objects.count()
                serial_num = prev_serial_num + 1 #Get next serial number to display in email

                dept = self.request.user.profile.department
                prof = Profile.objects.get(department=f'{dept}',level='2')
                em = prof.email #Gets email account of the HOD from the logged in user's department

                email = EmailMessage(
                subject=f'{form.instance.department} department R.T.S form',
                body=f'Waste Delivery Note number {serial_num} has been submitted by {form.instance.author}, kindly log on to the portal on http://10.10.1.195:8000/forms/home/ to view it.  In case of any challenges feel free to contact IT for further assistance.',
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

    # def form_valid(self,form):
    #     if 'elevate' in self.request.POST:
    #         form.instance.author = self.request.user #Inserts the author into the new post
    #         form.instance.department = self.request.user.profile.department

    #         prev_serial_num = WasteForm.objects.count()
    #         serial_num = prev_serial_num + 1 #Get next serial number to display in email

    #         dept = self.request.user.profile.department
    #         prof = Profile.objects.get(department=f'{dept}',level='2')
    #         em = prof.email #Gets email account of the HOD from the logged in user's department

    #         email = EmailMessage(
    #         subject=f'{form.instance.department} department R.T.S form',
    #         body=f'Waste Delivery Note number {serial_num} has been submitted by {form.instance.author}, kindly log on to the portal on http://10.10.1.195:8000/forms/home/ to view it.  In case of any challenges feel free to contact IT for further assistance.',
    #         from_email=config('EMAIL_HOST_USER'),
    #         # to=[f'{em}'],
    #         to=[config('BRIAN_EMAIL')],
    #         cc=[config('BRIAN_EMAIL')],
    #         reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
    #         )
    #         # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
    #         email.send()
    #         # messages.success(self.request, 'Form submitted and mail sent!')
    #         return super().form_valid(form)          