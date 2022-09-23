from django.shortcuts import redirect, render
from .models import checklist, waste_delivery_note, kgrn, goods_issue_note
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from datetime import date, datetime
from .forms import WasteForm, GoodsIssueNoteForm
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
import nums_from_string
import locale
locale.setlocale(locale.LC_ALL, '')

def dnotes_render_pdf_view(request, *args, **kwargs):
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

def goods_issue_note_render_pdf_view(request, *args, **kwargs):
   pk = kwargs.get('pk')
   gin = get_object_or_404(goods_issue_note, pk=pk)

   template_path = 'waste_management/generate_I_gin_pdf.html'
   context = {'gin': gin}
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

def goods_issue_note_external_render_pdf_view(request, *args, **kwargs):
   pk = kwargs.get('pk')
   gin = get_object_or_404(goods_issue_note, pk=pk)

   template_path = 'waste_management/generate_E_gin_pdf.html'
   context = {'gin': gin}
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

def checklists_render_pdf_view(request, *args, **kwargs):
   pk = kwargs.get('pk')
   checks = get_object_or_404(checklist, pk=pk)
   my_stringlist = checks.form_serials #Pick list of serial numbers from the checklist as a string
   print(f'Initial list {my_stringlist} type {type(my_stringlist)}')
   #my_list = my_stringlist.strip('][').split(',') #Split the string into list of individual items but each item as a string
   my_list = [nums_from_string.get_nums(my_stringlist)] #Split the string into list of individual items as integers
   print(f'Second list {my_list} type {type(my_list)}')
   my_list = [x for xs in my_list for x in xs] #Flatten the list of lists into a single list
   print(f'Third list {my_list} type {type(my_list)}')

   dnotes_list = []
   for num in my_list: #For each item in the new list
    dnote = get_object_or_404(waste_delivery_note, pk=num) #Find the corresponding delivery note
    print(f'{num} {dnote}')
    dnotes_list.append(dnote) #Add the delivery note to the list
    print(f'{dnotes_list}')

   template_path = 'waste_management/generatechecklist_pdf.html'
   context = {'dnotes_list': dnotes_list, 'checks': checks, 'dnote': dnote}
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
        form.instance.hod = self.request.user #Inserts the author into the new post
        if ('elevate' in self.request.POST) and (form.instance.form_status == 2): #If the HOD has clicked the button to elevate the form to the next level
            form.instance.form_status += 2 #Increases the form status by 2

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

        else:
            return HttpResponse('Error')

class DnoteWHUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/dnote_update1.html'
    model = waste_delivery_note
    fields = ['warehouse_hod_comment']

    def form_valid(self, form):
        form.instance.warehouse_hod = self.request.user

        if ('elevate' in self.request.POST) and (form.instance.form_status == 8): #If the WH HOD has clicked the button to elevate the form to the next level
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


        if ('demote' in self.request.POST) and (form.instance.form_status == 8): #
            form.instance.form_status -= 1 #If the WH HOD has clicked the button to demote the form to the previous level

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

        else:
            return HttpResponse('Error')

def create_checklist(request):
    if request.method == 'POST':
        check = request.POST.getlist('checks[]')
        print(f'Initial list {check} type {type(check)}')
        checklist_instance = checklist.objects.create(form_serials = check, date_posted = datetime.now(), author = request.user)
        checklist_instance.save()

        for num in check:
            waste_delivery_note.objects.filter(id=num).update(form_status=6)
    return redirect('checklists')  

def accept_checklist(request):
    if request.method == 'POST':
        check = request.POST.getlist('checks[]') #get the list of serial numbers
        print(f'Checklist IDs list {check} type {type(check)}')

        my_list_string = []
        my_list_int = []
        for num in check: #for each serial number in the list
            x = get_object_or_404(checklist, pk=num) #get the object for that serial number
            my_list_string.append(x.form_serials) #append the serial number to the list
        print(f'Initial list {my_list_string} type {type(my_list_string)}')

        for num in my_list_string: #for each serial number in the list
            my_list_int.append(nums_from_string.get_nums(num)) #append the serial number to the list, as an integer
        print(f'Final list {my_list_int} type {type(my_list_int)}')

        my_list_flat = [x for xs in my_list_int for x in xs] #Flatten the list of lists into a single list
        print(f'Y list {my_list_flat} type {type(my_list_flat)}')

        for num in check: #for each serial number in the list
            checklist.objects.filter(id=num).update(checklist_status=2) #update the checklist status to 2, meaning accepted, could also be done when extracting form serials from the list


        for num in my_list_flat: #for each serial number in the list
            waste_delivery_note.objects.filter(id=num).update(form_status=8, waste_offloader=request.user) #update the form status to 8, meaning accepted

    return redirect('checklists')

class CheckListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'checklists'
    template_name = 'waste_management/checklists.html'

    def get_queryset(self):
        return models.checklist.objects.all()  

class Dnotes_KGRN_ListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'waste_delivery_notes'
    template_name = 'waste_management/raise_kgrn.html'

    def get_queryset(self):
        return models.waste_delivery_note.objects.all() 

def create_kgrn(request):
    if request.method == 'POST':
        check = request.POST.getlist('checks[]')
        print(f'Initial list {check} type {type(check)}')
        kgrn_instance = kgrn.objects.create(form_serials = check, date_posted = datetime.now(), author = request.user)
        kgrn_instance.save()

    return redirect('dnotes_kgrn')

class KGRNListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'kgrns'
    template_name = 'waste_management/kgrns.html'

    def get_queryset(self):
        return models.kgrn.objects.all()

class KGRNHODUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_kgrn_hod.html'
    model = kgrn
    fields = ['hod_comment']

    def get_context_data(self, *args, **kwargs):
        pk = kwargs.get('pk')
        checks = get_object_or_404(kgrn, pk=pk)
        my_stringlist = checks.form_serials #Pick list of serial numbers from the checklist as a string
        print(f'Initial list {my_stringlist} type {type(my_stringlist)}')
        #my_list = my_stringlist.strip('][').split(',') #Split the string into list of individual items but each item as a string
        my_list = [nums_from_string.get_nums(my_stringlist)] #Split the string into list of individual items as integers
        print(f'Second list {my_list} type {type(my_list)}')
        my_list = [x for xs in my_list for x in xs] #Flatten the list of lists into a single list
        print(f'Third list {my_list} type {type(my_list)}')

        dnotes_list = []
        for num in my_list: #For each item in the new list
            dnote = get_object_or_404(waste_delivery_note, pk=num) #Find the corresponding delivery note
            print(f'{num} {dnote}')
            dnotes_list.append(dnote) #Add the delivery note to the list
            print(f'{dnotes_list}')

        template_path = 'waste_management/approve_kgrn_hod.html'
        context = {'dnotes_list': dnotes_list, 'checks': checks, 'dnote': dnote}
        return context

    def form_valid(self, form):
        form.instance.hod = self.request.user #Inserts the author into the new post
        if ('elevate' in self.request.POST) and (form.instance.form_status == 2): #If the HOD has clicked the button to elevate the form to the next level
            form.instance.form_status += 2 #Increases the form status by 2

            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
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
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
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
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.id} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
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
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.id} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=config('EMAIL_HOST_USER'),
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        else:
            return HttpResponse('Error')

class goods_issue_noteCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'waste_management/raise_goodsissuenote.html'
    success_message = 'Form Submitted Successfully!'
    model = goods_issue_note
    form_class = GoodsIssueNoteForm

    def form_valid(self,form):
        #Calculate total cost
        if form.instance.item1 != None:
            if form.instance.item_qty1_sale != None:
                i1 = round(form.instance.item_qty1_sale * form.instance.item1.price, 2)
            else:
                i1 = round(form.instance.item_qty1 * form.instance.item1.price, 2)
        else:
            i1 = 0
        if form.instance.item2 != None:
            if form.instance.item_qty2_sale != None:
                i2 = round(form.instance.item_qty2_sale * form.instance.item2.price, 2)
            else:
                i2 = round(form.instance.item_qty2 * form.instance.item2.price, 2)
        else:
            i2 = 0
        if form.instance.item3 != None:
            if form.instance.item_qty3_sale != None:
                i3 = round(form.instance.item_qty3_sale * form.instance.item3.price, 2)
            else:
                i3 = round(form.instance.item_qty3 * form.instance.item3.price, 2)
        else:
            i3 = 0
        if form.instance.item4 != None:
            if form.instance.item_qty4_sale != None:
                i4 = round(form.instance.item_qty4_sale * form.instance.item4.price, 2)
            else:
                i4 = round(form.instance.item_qty4 * form.instance.item4.price, 2)
        else:   
            i4 = 0
        if form.instance.item5 != None:
            if form.instance.item_qty5_sale != None:
                i5 = round(form.instance.item_qty5_sale * form.instance.item5.price, 2)
            else:
                i5 = round(form.instance.item_qty5 * form.instance.item5.price, 2)
        else:
            i5 = 0
        if form.instance.item6 != None:
            if form.instance.item_qty6_sale != None:
                i6 = round(form.instance.item_qty6_sale * form.instance.item6.price, 2)
            else:
                i6 = round(form.instance.item_qty6 * form.instance.item6.price, 2)
        else:
            i6 = 0
        if form.instance.item7 != None:
            if form.instance.item_qty7_sale != None:
                i7 = round(form.instance.item_qty7_sale * form.instance.item7.price, 2)
            else:
                i7 = round(form.instance.item_qty7 * form.instance.item7.price, 2)
        else:
            i7 = 0
        if form.instance.item8 != None:
            if form.instance.item_qty8_sale != None:
                i8 = round(form.instance.item_qty8_sale * form.instance.item8.price, 2)
            else:
                i8 = round(form.instance.item_qty8 * form.instance.item8.price, 2)
        else:
            i8 = 0
 
        result = round(i1 + i2 + i3 + i4 + i5 + i6 + i7 + i8, 2)

        form.instance.gross_total = result * int(1.16)

        form.instance.my_total = result

        if form.instance.isInternal == True:
            form.instance.form_status = 2 #Increases the form status by 2
        else:
            form.instance.form_status = 1 #Increases the form status by 1

        form.instance.author = self.request.user #Inserts the author into the new post
        form.instance.department_from = self.request.user.profile.department

        prev_serial_num = goods_issue_note.objects.count()
        serial_num = prev_serial_num + 1 #Get next serial number to display in email

        #form.instance.id = serial_num #Inserts the serial number into the new post

        dept = self.request.user.profile.department
        prof = Profile.objects.get(department=f'{dept}',level='2')
        em = prof.email #Gets email account of the HOD from the logged in user's department
 
        email = EmailMessage(
        subject=f'{form.instance.department_from} department Goods Issue Note',
        body=f'Goods Issue Note number {serial_num} has been submitted by {form.instance.author}.\nKindly log on to the portal to view it.\vIn case of any challenges, feel free to contact IT for further assistance.',
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

class HOD_goods_issue_noteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_hod_gin.html'
    model = goods_issue_note
    fields = ['hod_comment']

    # def get_context_data(self, **kwargs):
    #     context = {'my_variable': 0}
    #     return context

    def form_valid(self, form):
        form.instance.hod = self.request.user
        
        #print(form.instance.item_qty8)
        #print(form.instance.item_qty8_sale)

        if ('elevate' in self.request.POST) and (form.instance.form_status == 2): #For internal forms, if the form is approved by the HOD, the form status is increased by 2
            form.instance.form_status += 2 

            return super().form_valid(form)

        if ('elevate' in self.request.POST) and (form.instance.form_status == 1): #For external forms, if the form is approved by the HOD, the form status is increased by 2
            form.instance.form_status += 2 

            return super().form_valid(form)    


        if ('demote' in self.request.POST) and (form.instance.form_status == 2): #For internal forms, if the form is rejected by the HOD, the form status is decreased by 2
            form.instance.form_status -= 2 

            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 1): #For external forms, if the form is rejected by the HOD, the form status is decreased by 1
            form.instance.form_status -= 1 

            return super().form_valid(form)  

        else:
            return HttpResponse('Error')

class FM_goods_issue_noteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_goodsissuenote.html'
    model = goods_issue_note
    fields = ['fm_comment']

    # def get_context_data(self, **kwargs):
    #     context = {'my_variable': 0}
    #     return context

    def form_valid(self, form):
        form.instance.approved_by = self.request.user
        
        #print(form.instance.item_qty8)
        #print(form.instance.item_qty8_sale)

        if ('elevate' in self.request.POST) and (form.instance.form_status == 4): #For internal forms, if the form is approved by the FM, the form status is increased by 2
            form.instance.form_status += 2 

            return super().form_valid(form)

        if ('elevate' in self.request.POST) and (form.instance.form_status == 3): #For external forms, if the form is approved by the FM, the form status is increased by 2
            form.instance.form_status += 2 

            return super().form_valid(form)    


        if ('demote' in self.request.POST) and (form.instance.form_status == 2): #For internal forms, if the form is rejected by the FM, the form status is decreased by 2
            form.instance.form_status -= 2 

            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 1): #For external forms, if the form is rejected by the FM, the form status is decreased by 1
            form.instance.form_status -= 1 

            return super().form_valid(form)  

        else:
            return HttpResponse('Error')


class Dept_goods_issue_noteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/dept_receivegoodsissuenote.html'
    model = goods_issue_note
    fields = ['received_by','dept_comment']

    def form_valid(self, form):
        form.instance.approved_by = self.request.user

        if ('elevate' in self.request.POST) and (form.instance.form_status == 6):
            form.instance.form_status += 2 

            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 6):
            form.instance.form_status -= 6 

            return super().form_valid(form)

        else:
            return HttpResponse('Error')

class Sales_goods_issue_noteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/sales_receivegoodsissuenote.html'
    model = goods_issue_note
    fields = ['item_qty1_sale','item_qty2_sale','item_qty3_sale','item_qty4_sale','item_qty5_sale','item_qty6_sale','item_qty7_sale','item_qty8_sale','received_by','dept_comment']
    # form_class = GoodsIssueNoteForm

    def form_valid(self, form):
        # Calculate updated total price
        if form.instance.item1 != None:
            if form.instance.item_qty1_sale != None:
                i1 = round(form.instance.item_qty1_sale * form.instance.item1.price, 2)
            else:
                i1 = round(form.instance.item_qty1 * form.instance.item1.price, 2)
        else:
            i1 = 0
        if form.instance.item2 != None:
            if form.instance.item_qty2_sale != None:
                i2 = round(form.instance.item_qty2_sale * form.instance.item2.price, 2)
            else:
                i2 = round(form.instance.item_qty2 * form.instance.item2.price, 2)
        else:
            i2 = 0
        if form.instance.item3 != None:
            if form.instance.item_qty3_sale != None:
                i3 = round(form.instance.item_qty3_sale * form.instance.item3.price, 2)
            else:
                i3 = round(form.instance.item_qty3 * form.instance.item3.price, 2)
        else:
            i3 = 0
        if form.instance.item4 != None:
            if form.instance.item_qty4_sale != None:
                i4 = round(form.instance.item_qty4_sale * form.instance.item4.price, 2)
            else:
                i4 = round(form.instance.item_qty4 * form.instance.item4.price, 2)
        else:   
            i4 = 0
        if form.instance.item5 != None:
            if form.instance.item_qty5_sale != None:
                i5 = round(form.instance.item_qty5_sale * form.instance.item5.price, 2)
            else:
                i5 = round(form.instance.item_qty5 * form.instance.item5.price, 2)
        else:
            i5 = 0
        if form.instance.item6 != None:
            if form.instance.item_qty6_sale != None:
                i6 = round(form.instance.item_qty6_sale * form.instance.item6.price, 2)
            else:
                i6 = round(form.instance.item_qty6 * form.instance.item6.price, 2)
        else:
            i6 = 0
        if form.instance.item7 != None:
            if form.instance.item_qty7_sale != None:
                i7 = round(form.instance.item_qty7_sale * form.instance.item7.price, 2)
            else:
                i7 = round(form.instance.item_qty7 * form.instance.item7.price, 2)
        else:
            i7 = 0
        if form.instance.item8 != None:
            if form.instance.item_qty8_sale != None:
                i8 = round(form.instance.item_qty8_sale * form.instance.item8.price, 2)
            else:
                i8 = round(form.instance.item_qty8 * form.instance.item8.price, 2)
        else:
            i8 = 0
 
        result = round(i1 + i2 + i3 + i4 + i5 + i6 + i7 + i8, 2)

        form.instance.my_total = result

        form.instance.total_cost = result * int(1.16)

        form.instance.received_by = self.request.user

        if ('elevate' in self.request.POST) and (form.instance.form_status == 5):
            form.instance.form_status += 2
            print(2) 

            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 5):
            form.instance.form_status -= 5 

            return super().form_valid(form)
        else:
            return HttpResponse('Error')

class Goods_issue_note_ListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'goods_issue_notes'
    template_name = 'waste_management/gins.html'

    def get_queryset(self):
        return models.goods_issue_note.objects.all() 