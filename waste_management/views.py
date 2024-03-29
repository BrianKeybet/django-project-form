import itertools
from io import BytesIO
from django.db.models import Q
from django.conf import settings
from decouple  import config
from .models import Checklist, waste_delivery_note, kgrn, GoodsIssueNote, kgrn_item
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from datetime import datetime
from .forms import WasteForm, GoodsIssueNoteForm, KGRNForm
from users.models import Profile
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView
from django.shortcuts import get_object_or_404, redirect, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import nums_from_string
import locale
locale.setlocale(locale.LC_ALL, '')
from .filters import *


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
   gin = get_object_or_404(GoodsIssueNote, pk=pk)

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
   gin = get_object_or_404(GoodsIssueNote, pk=pk)

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
   checks = get_object_or_404(Checklist, pk=pk)
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

def kgrns_render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    checks = get_object_or_404(kgrn, pk=pk)
    my_stringlist = checks.form_serials #Pick list of serial numbers from the checklist as a string
    my_list = [nums_from_string.get_nums(my_stringlist)] #Split the string into list of individual items as integers
    my_list = [x for xs in my_list for x in xs] #Flatten the list of lists into a single list

    dnotes_list = waste_delivery_note.objects.filter(pk__in=my_list)

    # Create a list of material names and quantities for each delivery note
    notes_with_materials = []
    for dnote in dnotes_list:
        for i in range(1, 9):
            item_name = getattr(dnote, f"item{i}")
            if item_name:
                material_obj = Material.objects.get(name=item_name)
                item_name_cleaned = item_name.name.replace("/", "")
                notes_with_materials.append((item_name_cleaned, getattr(dnote, f"item_qty{i}"), material_obj.uom))
            else:
                break
    notes_with_materials = sorted(notes_with_materials, key=lambda n: n[0]) #Sort to ensure groupby doesn't skip any materials
    print(f'my_materials{notes_with_materials}')
    # Group the delivery notes by material name
    dnotes_by_material = {}
    for material, notes in itertools.groupby(notes_with_materials, key=lambda n: n[0]):
        qty_list = []
        uom = None
        for note in notes:
            qty_list.append(note[1])
            if uom is None:
                uom = note[2]
            elif uom != note[2]:
                raise ValueError("Inconsistent uom values for material")
            total_qty = sum(qty_list)
            total_qty = round(total_qty, 2)
        dnotes_by_material[material] = {'quantity': total_qty, 'uom': uom}

    template_path = 'waste_management/generatekgrn_pdf.html'
    # context = {'checks': checks, 'dnote': dnote, 'notes_with_materials': notes_with_materials}
    context = {'checks': checks, 'dnote': dnote, 'materials': dnotes_by_material}
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

def blank_kgrns_render_pdf_view(request, *args, **kwargs):
   pk = kwargs.get('pk')
   bkgrn = get_object_or_404(kgrn_item, pk=pk)

   template_path = 'waste_management/generate_bkgrn_pdf.html'
   context = {'bkgrn': bkgrn}
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

        dept = self.request.user.profile.department_id
        profs = Profile.objects.filter(department=f'{dept}',level='2')

        print(f'Profiles {profs}')
        for prof in profs:
            print(f'Each email: {prof.user.email}')
            print(f'Each name: {prof.user.first_name}')
            print(f'Host email: {settings.EMAIL_HOST_USER}')
            subject = 'Waste Delivery Note'
            message = f'Hello {prof.user.first_name}, a new Waste Delivery Note number {serial_num} has been submitted for your approval. \nPlease login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.'
            email_from = settings.EMAIL_HOST_USER
            #recipient_list = [prof.user.email, config('BRIAN_EMAIL'), config('BRIAN_EMAIL')]
            recipient_list = [config('BRIAN_EMAIL')]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

        return super().form_valid(form)

class DnotesListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'waste_delivery_notes'
    template_name = 'waste_management/waste_dnotes_list.html'
    paginate_by: int = 10
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = waste_delivery_noteFilter(self.request.GET, queryset=self.get_queryset())
        my_department = str(self.request.user.profile.department)
        context['my_department'] = my_department
        return context

    def get_queryset(self):
        return waste_delivery_note.objects.all()           

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
            body=f'Waste delivery note number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on to create checklist http://10.10.0.173:8000/waste/dnotes/ .\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.author.profile.email],
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
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.author.profile.email],
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
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.author.profile.email],
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
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.author.profile.email],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        else:
            return HttpResponse('Error : Form has already been approved or rejected')

class DnoteWHUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/dnote_update1.html'
    model = waste_delivery_note
    fields = ['warehouse_hod_comment']

    def form_valid(self, form):
        form.instance.warehouse_hod = self.request.user

        dept = form.instance.author.profile.department_id
        profs = Profile.objects.filter(department=f'{dept}',level='2')

        if ('elevate' in self.request.POST) and (form.instance.form_status == 8): #If the WH HOD has clicked the button to elevate the form to the next level
            form.instance.form_status += 2

            for prof in profs:
                subject = 'Waste Delivery Note'
                message = f'Hello {prof.user.first_name}, Waste delivery note number {form.instance.id} submitted by {form.instance.author} has been approved by {self.request.user}. Please login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.'
                email_from = settings.EMAIL_HOST_USER
                #recipient_list = [prof.user.email, config('BRIAN_EMAIL')]
                recipient_list = [config('BRIAN_EMAIL')]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
           
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 8): #
            form.instance.form_status -= 1 #If the WH HOD has clicked the button to demote the form to the previous level

            for prof in profs:
                subject = 'Waste Delivery Note'
                message = f'Hello {prof.user.first_name}, Waste delivery note number {form.instance.id} submitted by {form.instance.author} has been rejected by {self.request.user}. Please login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.'
                email_from = settings.EMAIL_HOST_USER
                #recipient_list = [prof.user.email, config('BRIAN_EMAIL')]
                recipient_list = [config('BRIAN_EMAIL')]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        else:
            return HttpResponse('Error : Form has already been approved or rejected')

def create_checklist(request):
    if request.method == 'POST':
        check = request.POST.getlist('checks[]')
        print(f'Initial list {check} type {type(check)}')
        # Get list of integers and separate them with commas
        new_check = ', '.join((map(str,check)))
        if len(check) == 0:
            return HttpResponse('Error: No items selected')
        else:
            checklist_instance = Checklist.objects.create(form_serials = new_check, date_posted = datetime.now(), author = request.user)
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
            x = get_object_or_404(Checklist, pk=num) #get the object for that serial number
            my_list_string.append(x.form_serials) #append the serial number to the list
        print(f'Initial list {my_list_string} type {type(my_list_string)}')

        for num in my_list_string: #for each serial number in the list
            my_list_int.append(nums_from_string.get_nums(num)) #append the serial number to the list, as an integer
        print(f'Final list {my_list_int} type {type(my_list_int)}')

        my_list_flat = [x for xs in my_list_int for x in xs] #Flatten the list of lists into a single list
        #Convert to comma separated integers
        my_list_email = ', '.join((map(str,my_list_flat)))
        print(f'Y list {my_list_flat} type {type(my_list_flat)}')

        for num in check: #for each serial number in the list
            Checklist.objects.filter(id=num).update(checklist_status=2) #update the checklist status to 2, meaning accepted, could also be done when extracting form serials from the list


        for num in my_list_flat: #for each serial number in the list
            waste_delivery_note.objects.filter(id=num).update(form_status=8, waste_offloader=request.user) #update the form status to 8, meaning accepted

        dept = request.user.profile.department_id
        profs = Profile.objects.filter(department=f'{dept}',level='2')

        for prof in profs:
            subject = 'Waste Delivery Note'
            message = f'Hello {prof.user.first_name}, Waste delivery note number(s) {my_list_email} has been accepted by {request.user}. Please login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.'
            email_from = settings.EMAIL_HOST_USER
            #recipient_list = [prof.user.email, config('BRIAN_EMAIL')]
            recipient_list = [config('BRIAN_EMAIL')]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

    return redirect('checklists')

class CheckListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'checklists'
    template_name = 'waste_management/checklists.html'
    paginate_by: int = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ChecklistFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        return Checklist.objects.all()  

class Dnotes_KGRN_ListView(LoginRequiredMixin, generic.ListView):

    context_object_name = 'waste_delivery_notes'
    #context_object_name = 'raise_kgrns'
    template_name = 'waste_management/raise_kgrn.html'

    #paginate_by = 3


    def get_queryset(self):
        return waste_delivery_note.objects.all() 

def create_kgrn(request):
    if request.method == 'POST':
        check = request.POST.getlist('checks[]')
        # print(f'Initial list {check} type {type(check)}')
        # Get list of integers and separate them with commas
        new_check = ', '.join((map(str,check)))
        # print(f'Second list {new_check} type {type(check)}')
        # print(f'My_dept{request.user.profile.department} type {type(request.user.profile.department)}')

        kgrn_sum = kgrn_item.objects.count()
        kgrn_sum1 = kgrn.objects.count()
        serial_num = kgrn_sum + kgrn_sum1 + 37 #Get next serial number to display in email

        for num in check:
            waste_delivery_note.objects.filter(id=num).update(form_status=11) #Removes the form from the list of forms at KGRN create stage
            supplier = str(waste_delivery_note.objects.get(id=num).supplier) #Get the supplier for the form and convert to string

            # print(f'Supplier {supplier} type {type(supplier)}')

        kgrn_instance = kgrn.objects.create(serial_num = serial_num, form_serials = new_check, date_posted = datetime.now(), author = request.user, department = str(request.user.profile.department), supplier = supplier)
        kgrn_instance.save()


    return redirect('kgrns')

class KGRNListView(LoginRequiredMixin, ListView):
    context_object_name = 'kgrns'
    template_name = 'waste_management/kgrns.html'
    paginate_by: int = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = kgrnFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self, *args, **kwargs):
        return kgrn.objects.all()

class KGRNStocksUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/update_kgrn_stock.html'
    model = kgrn
    fields = ['collected_by','id_number', 'vehicle_no']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        checks = kgrn.objects.get(pk=pk)
        my_stringlist = checks.form_serials #Pick list of serial numbers from the checklist as a string
        my_list = [nums_from_string.get_nums(my_stringlist)] #Split the string into list of individual items as integers
        my_list = [x for xs in my_list for x in xs] #Flatten the list of lists into a single list

        dnotes_list = waste_delivery_note.objects.filter(pk__in=my_list)

        # Create a list of material names and quantities for each delivery note
        notes_with_materials = []
        for dnote in dnotes_list:
            for i in range(1, 9):
                item_name = getattr(dnote, f"item{i}")
                if item_name:
                    # item_name_cleaned = item_name.name.replace(" ", "").replace("/", "")
                    item_name_cleaned = item_name.name.replace("/", "")
                    notes_with_materials.append((item_name_cleaned, getattr(dnote, f"item_qty{i}")))
                else:
                    break
        notes_with_materials = sorted(notes_with_materials, key=lambda n: n[0]) #Sort to ensure groupby doesn't skip any materials
        # Group the delivery notes by material name
        dnotes_by_material = {}
        for material, notes in itertools.groupby(notes_with_materials, key=lambda n: n[0]):
            qty_list = [n[1] for n in notes]
            total_qty = sum(qty_list)
            total_qty = round(total_qty, 2)
            dnotes_by_material[material] = total_qty
            #print(f'initial aggregation:{dnotes_by_material}')

        context.update({'checks': checks, 'dnote': dnote, 'materials': dnotes_by_material})
        return context

    def form_valid(self, form):
        profs = Profile.objects.filter(level='2')

        if ('elevate' in self.request.POST) and (form.instance.kgrn_status == 0): #If the HOD has clicked the button to elevate the form to the next level
            form.instance.kgrn_status += 15 #Increases the form status by 0.5

            dept = self.request.user.profile.department_id
            profs = Profile.objects.filter(department=f'{dept}',level='2')

            for prof in profs:
                subject = 'KGRN (D/Notes)'
                html_message = f'Hello {prof.user.first_name}, a new D/Notes based KGRN has been submitted for your approval.\nPlease login to the system on http://10.10.0.173:8000/waste/kgrns/ to view the form. \n The serial number is {form.instance.serial_num} \n Issued to: {form.instance.supplier} \n Vehicle number: {form.instance.vehicle_no}.'
                email_from = settings.EMAIL_HOST_USER
                #recipient_list = [prof.user.email, config('BRIAN_EMAIL'), config('BRIAN_EMAIL')]
                recipient_list = [config('BRIAN_EMAIL')]
                send_mail(subject, html_message, email_from, recipient_list, fail_silently=False)

            messages.success(self.request, f'Form submitted and mail sent just now!')
            return super().form_valid(form)

        else:
            return HttpResponse('Error : Form has already been approved or rejected')

class KGRNHODUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_kgrn_hod.html'
    model = kgrn
    fields = ['hod_comment']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        checks = kgrn.objects.get(pk=pk)
        my_stringlist = checks.form_serials #Pick list of serial numbers from the checklist as a string
        my_list = [nums_from_string.get_nums(my_stringlist)] #Split the string into list of individual items as integers
        my_list = [x for xs in my_list for x in xs] #Flatten the list of lists into a single list

        dnotes_list = waste_delivery_note.objects.filter(pk__in=my_list)

        # Create a list of material names and quantities for each delivery note
        notes_with_materials = []
        for dnote in dnotes_list:
            for i in range(1, 9):
                item_name = getattr(dnote, f"item{i}")
                if item_name:
                    # item_name_cleaned = item_name.name.replace(" ", "").replace("/", "")
                    item_name_cleaned = item_name.name.replace("/", "")
                    notes_with_materials.append((item_name_cleaned, getattr(dnote, f"item_qty{i}")))
                else:
                    break
        notes_with_materials = sorted(notes_with_materials, key=lambda n: n[0]) #Sort to ensure groupby doesn't skip any materials
        # Group the delivery notes by material name
        dnotes_by_material = {}
        for material, notes in itertools.groupby(notes_with_materials, key=lambda n: n[0]):
            qty_list = [n[1] for n in notes]
            total_qty = sum(qty_list)
            total_qty = round(total_qty, 2)
            dnotes_by_material[material] = total_qty
            #print(f'initial aggregation:{dnotes_by_material}')

        context.update({'checks': checks, 'dnote': dnote, 'materials': dnotes_by_material})
        return context

    def form_valid(self, form, **kwargs):
        form.instance.hod = self.request.user #Inserts the author into the new post
        # profs = Profile.objects.filter(level='4').select_related('user')
        profs = Profile.objects.filter(Q(level='1') & Q(department_id='14') | Q(level='4')).select_related('user')
        director_profile = Profile.objects.filter(email=config('PUR_DIR_EMAIL')).select_related('user')
        profs = profs | director_profile #Combine the two querysets


        if ('elevate' in self.request.POST) and (form.instance.kgrn_status == 15): #If the HOD has clicked the button to elevate the form to the next level
            form.instance.kgrn_status -= 13 #Reduce the form status by 13

            for prof in profs:
                email = EmailMessage(
                subject=f'{form.instance.department} department KGRN(D/Notes)',
                body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/ to view it. \n The serial number is {form.instance.serial_num} \n Issued to: {form.instance.supplier} \n Vehicle number: {form.instance.vehicle_no}.\nIn case of any challenges, feel free to contact IT for further assistance.',
                from_email=settings.EMAIL_HOST_USER,
                to=[config('BRIAN_EMAIL')],
                cc=[config('BRIAN_EMAIL')],
                reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
                )
                # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
                email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        if ('elevate' in self.request.POST) and (form.instance.kgrn_status == 3):
            form.instance.kgrn_status += 1
            
            for prof in profs:
                email = EmailMessage(
                subject=f'{form.instance.department} department KGRN',
                body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/ to view it. \n The serial number is {form.instance.serial_num} \n Issued to: {form.instance.supplier} \n Vehicle number: {form.instance.vehicle_no}.\nIn case of any challenges, feel free to contact IT for further assistance.',
                from_email=settings.EMAIL_HOST_USER,
                #to=[prof.user.email],
                to=[config('BRIAN_EMAIL')],
                cc=[config('BRIAN_EMAIL')],
                reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
                )
                # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
                email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.kgrn_status == 2):
            form.instance.kgrn_status -= 1

            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/ to view it. \n The serial number is {form.instance.serial_num} \n Issued to: {form.instance.supplier} \n Vehicle number: {form.instance.vehicle_no}.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.author.profile.email],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        if ('demote' in self.request.POST) and (form.instance.kgrn_status == 3):
            form.instance.kgrn_status -= 2

            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/ to view it. \n The serial number is {form.instance.serial_num} \n Issued to: {form.instance.supplier} \n Vehicle number: {form.instance.vehicle_no}.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.author.profile.email],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        else:
            return HttpResponse('Error : Form has already been approved or rejected')

class KGRNPurchaseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_kgrn_purchase.html'
    model = kgrn
    fields = ['resolution','purchase_comment']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        checks = kgrn.objects.get(pk=pk)
        my_stringlist = checks.form_serials #Pick list of serial numbers from the checklist as a string
        my_list = [nums_from_string.get_nums(my_stringlist)] #Split the string into list of individual items as integers
        my_list = [x for xs in my_list for x in xs] #Flatten the list of lists into a single list

        dnotes_list = waste_delivery_note.objects.filter(pk__in=my_list)

        # Create a list of material names and quantities for each delivery note
        notes_with_materials = []
        for dnote in dnotes_list:
            for i in range(1, 9):
                item_name = getattr(dnote, f"item{i}")
                if item_name:
                    # item_name_cleaned = item_name.name.replace(" ", "").replace("/", "")
                    item_name_cleaned = item_name.name.replace("/", "")
                    notes_with_materials.append((item_name_cleaned, getattr(dnote, f"item_qty{i}")))
                else:
                    break
        notes_with_materials = sorted(notes_with_materials, key=lambda n: n[0]) #Sort to ensure groupby doesn't skip any materials
        # Group the delivery notes by material name
        dnotes_by_material = {}
        for material, notes in itertools.groupby(notes_with_materials, key=lambda n: n[0]):
            qty_list = [n[1] for n in notes]
            total_qty = sum(qty_list)
            total_qty = round(total_qty, 2)
            dnotes_by_material[material] = total_qty
            #print(f'initial aggregation:{dnotes_by_material}')

        context.update({'checks': checks, 'dnote': dnote, 'materials': dnotes_by_material})

        return context

    def form_valid(self, form):
        form.instance.purchase_rep = self.request.user #Inserts the author into the new post

        response = super().form_valid(form)  # Save the form data to the database

        if ('elevate' in self.request.POST) and (form.instance.kgrn_status == 2): #If the HOD has clicked the button to elevate the form to the next level
            form.instance.kgrn_status += 2 #Increases the form status by 2
            pdf = kgrns_render_pdf_view(self.request, pk=form.instance.id)

            prof = Supplier.objects.get(name=form.instance.supplier)
            emails = prof.email.values_list('email', flat=True)

            # Add PDF as attachment to each email
            subject = f'{form.instance.supplier} KGRN'
            message = f'Dear Sir/Madam,\n\nKindly find attached, your Goods’ Return Note number {form.instance.serial_num}.\n\nPlease contact us using the information provided below if you have any concerns, queries or need clarification.\n\n          Tel: +254 20 6420000\n          Email: purchase@kapa-oil.com\n\nThank you.'
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to = emails,
                cc= [config('BRIAN_EMAIL')],
                bcc= [config('BRIAN_EMAIL')],
                reply_to=[config('BRIAN_EMAIL')],
            )
            pdf_file = BytesIO(pdf.content)
            email.attach('report.pdf', pdf_file.getvalue(), 'application/pdf')
            email.send()

            messages.success(self.request, f'Form submitted and mail sent to {emails}')
            return super().form_valid(form)
            
        if ('elevate' in self.request.POST) and (form.instance.kgrn_status == 3):
            form.instance.kgrn_status += 1

            
            pdf = kgrns_render_pdf_view(self.request, pk=form.instance.id)

            prof = Supplier.objects.get(name=form.instance.supplier)
            emails = prof.email.values_list('email', flat=True)

            # Add PDF as attachment to each email
            subject = f'{form.instance.supplier} KGRN'
            message = f'Dear Sir/Madam,\n\nKindly find attached, your Goods’ Return Note number {form.instance.serial_num}.\n\nPlease contact us using the information provided below if you have any concerns, queries or need clarification.\n\n          Tel: +254 20 6420000\n          Email: purchase@kapa-oil.com\n\nThank you.'
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to = emails,
                cc= [config('BRIAN_EMAIL')],
                bcc = [config('BRIAN_EMAIL')],
                reply_to=[config('BRIAN_EMAIL')],
            )
            pdf_file = BytesIO(pdf.content)
            email.attach('report.pdf', pdf_file.getvalue(), 'application/pdf')
            email.send()

            messages.success(self.request, f'Form submitted and mail sent to {emails}')
            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.kgrn_status == 2):
            form.instance.kgrn_status -= 1

            messages.success(self.request,'Form submitted!')
            return super().form_valid(form)
            
        if ('demote' in self.request.POST) and (form.instance.kgrn_status == 3):
            form.instance.kgrn_status -= 2

            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.hod.profile.email],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        else:
            return HttpResponse('Error : Form has already been approved or rejected')
        
        return response

class KGRNPurchase2UpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_kgrn_purchase2.html'
    model = kgrn
    fields = ['pur_close_comment']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        checks = kgrn.objects.get(pk=pk)
        my_stringlist = checks.form_serials #Pick list of serial numbers from the checklist as a string
        my_list = [nums_from_string.get_nums(my_stringlist)] #Split the string into list of individual items as integers
        my_list = [x for xs in my_list for x in xs] #Flatten the list of lists into a single list

        dnotes_list = waste_delivery_note.objects.filter(pk__in=my_list)

        # Create a list of material names and quantities for each delivery note
        notes_with_materials = []
        for dnote in dnotes_list:
            for i in range(1, 9):
                item_name = getattr(dnote, f"item{i}")
                if item_name:
                    # item_name_cleaned = item_name.name.replace(" ", "").replace("/", "")
                    item_name_cleaned = item_name.name.replace("/", "")
                    notes_with_materials.append((item_name_cleaned, getattr(dnote, f"item_qty{i}")))
                else:
                    break
        notes_with_materials = sorted(notes_with_materials, key=lambda n: n[0]) #Sort to ensure groupby doesn't skip any materials
        # Group the delivery notes by material name
        dnotes_by_material = {}
        for material, notes in itertools.groupby(notes_with_materials, key=lambda n: n[0]):
            qty_list = [n[1] for n in notes]
            total_qty = sum(qty_list)
            total_qty = round(total_qty, 2)
            dnotes_by_material[material] = total_qty
            #print(f'initial aggregation:{dnotes_by_material}')

        context.update({'checks': checks, 'dnote': dnote, 'materials': dnotes_by_material})

        return context

    def form_valid(self, form):
        profs = Profile.objects.filter(level='6')

        if ('elevate' in self.request.POST) and (form.instance.kgrn_status == 4):
            form.instance.kgrn_status += 2 #Increases the form status by 2
            for prof in profs:
                email = EmailMessage(
                subject=f'{form.instance.department} department KGRN',
                body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
                from_email=settings.EMAIL_HOST_USER,
                #to=[prof.user.email],
                to=[config('BRIAN_EMAIL')],
                cc=[config('BRIAN_EMAIL')],
                reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
                )
                # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
                email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.kgrn_status == 4):
            form.instance.kgrn_status -= 2

            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            #to=[form.instance.hod.profile.email],
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()

            messages.success(self.request,'Form submitted')
            return super().form_valid(form)
            
        else:
            return HttpResponse('Error : Form has already been approved or rejected')

class CloseKGRNUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_kgrn_close.html'
    model = kgrn
    fields = ['accounts_comment']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        checks = kgrn.objects.get(pk=pk)
        my_stringlist = checks.form_serials #Pick list of serial numbers from the checklist as a string
        my_list = [nums_from_string.get_nums(my_stringlist)] #Split the string into list of individual items as integers
        my_list = [x for xs in my_list for x in xs] #Flatten the list of lists into a single list

        dnotes_list = waste_delivery_note.objects.filter(pk__in=my_list)

        # Create a list of material names and quantities for each delivery note
        notes_with_materials = []
        for dnote in dnotes_list:
            for i in range(1, 9):
                item_name = getattr(dnote, f"item{i}")
                if item_name:
                    # item_name_cleaned = item_name.name.replace(" ", "").replace("/", "")
                    item_name_cleaned = item_name.name.replace("/", "")
                    notes_with_materials.append((item_name_cleaned, getattr(dnote, f"item_qty{i}")))
                else:
                    break
        notes_with_materials = sorted(notes_with_materials, key=lambda n: n[0]) #Sort to ensure groupby doesn't skip any materials
        # Group the delivery notes by material name
        dnotes_by_material = {}
        for material, notes in itertools.groupby(notes_with_materials, key=lambda n: n[0]):
            qty_list = [n[1] for n in notes]
            total_qty = sum(qty_list)
            total_qty = round(total_qty, 2)
            dnotes_by_material[material] = total_qty
            #print(f'initial aggregation:{dnotes_by_material}')

        context.update({'checks': checks, 'dnote': dnote, 'materials': dnotes_by_material})

        return context
    def form_valid(self, form):
        form.instance.closed_by = self.request.user
        if ('elevate' in self.request.POST) and (form.instance.kgrn_status == 6): #If the button to elevate the form to the next level has been clicked
            form.instance.kgrn_status += 2 #Increases the form status by 2

            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been closed by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            #to=[form.instance.hod.profile.email, form.instance.author.profile.email],
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        if ('elevate' in self.request.POST) and (form.instance.kgrn_status == 5):
            form.instance.kgrn_status += 1
            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been closed by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            #to=[form.instance.hod.profile.email, form.instance.author.profile.email],
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.kgrn_status == 6):
            form.instance.kgrn_status -= 1

            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            #to=[form.instance.hod.profile.email, form.instance.author.profile.email],
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        if ('demote' in self.request.POST) and (form.instance.kgrn_status == 5):
            form.instance.kgrn_status -= 2

            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            #to=[form.instance.hod.profile.email, form.instance.author.profile.email],
            to=[config('BRIAN_EMAIL')],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        else:
            return HttpResponse('Error : Form has already been approved or rejected')

class BlankKGRN_CreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'waste_management/raise_blankkgrn.html'
    success_message = 'Form Submitted Successfully!'
    model = kgrn_item
    form_class = KGRNForm

    def form_valid(self,form):
        form.instance.form_status = 2 #Increases the form status by 2

        form.instance.author = self.request.user #Inserts the author into the new post
        form.instance.department = self.request.user.profile.department

        kgrn_sum = kgrn_item.objects.count()
        kgrn_sum1 = kgrn.objects.count()
        serial_num = kgrn_sum + kgrn_sum1 + 1 #Get next serial number to display in email

        form.instance.serial_num = serial_num

        dept = self.request.user.profile.department_id
        profs = Profile.objects.filter(department=f'{dept}',level='2')

        for prof in profs:
            subject = 'KGRN'
            message = f'Hello {prof.user.first_name},\nA new KGRN number {serial_num} has been submitted for your approval.\nPlease login to the system on http://10.10.0.173:8000/waste/kgrns/items/ to view the form.\n The serial number is {serial_num}.\n Issued to: {form.instance.supplier}.\n Vehicle number: {form.instance.vehicle_no}'
            email_from = settings.EMAIL_HOST_USER
            #recipient_list = [prof.user.email, config('BRIAN_EMAIL'), config('BRIAN_EMAIL')]
            recipient_list = [config('ICT_GMAIL')]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

        return super().form_valid(form)

class KGRN_ItemsListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'kgrn_items'
    template_name = 'waste_management/kgrn_items.html'
    paginate_by: int = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = kgrn_itemFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        return kgrn_item.objects.all()

class BlankKGRNHODUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_kgrn_item_hod.html'
    model = kgrn_item
    fields = ['hod_comment']

    def form_valid(self, form):
        form.instance.hod = self.request.user #Inserts the author into the new post
        profs = Profile.objects.filter(level='4')
        director_profile = Profile.objects.filter(email=config('PUR_DIR_EMAIL'))
        profs = profs | director_profile #Combine the two querysets

        if ('elevate' in self.request.POST) and (form.instance.form_status == 2): #If the HOD has clicked the button to elevate the form to the next level
            form.instance.form_status += 2 #Increases the form status by 2

            for prof in profs:    
                email = EmailMessage(
                subject=f'{form.instance.department} department KGRN',
                body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/items/ to view it.\n Issued to: {form.instance.supplier}.\n Vehicle number: {form.instance.vehicle_no}\nIn case of any challenges, feel free to contact IT for further assistance.',
                from_email=settings.EMAIL_HOST_USER,
                to=[prof.user.email],
                cc=[config('BRIAN_EMAIL'),config('WAREHOUSE_HOD')],
                reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
                )
                # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
                email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        if ('elevate' in self.request.POST) and (form.instance.form_status == 3):
            form.instance.form_status += 1

            for prof in profs:
                email = EmailMessage(
                subject=f'{form.instance.department} department KGRN',
                body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/items/ to view it.\n Issued to: {form.instance.supplier}.\n Vehicle number: {form.instance.vehicle_no}\nIn case of any challenges, feel free to contact IT for further assistance.',
                from_email=settings.EMAIL_HOST_USER,
                to=[prof.user.email],
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
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/items/ to view it.\n Issued to: {form.instance.supplier}.\n Vehicle number: {form.instance.vehicle_no}\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.author.profile.email],
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
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/items/ to view it.\n Issued to: {form.instance.supplier}.\n Vehicle number: {form.instance.vehicle_no}\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.author.profile.email],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        else:
            return HttpResponse('Error : Form has already been approved or rejected')

class BlankKGRNPurchaseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_kgrn_item_purchase.html'
    model = kgrn_item
    fields = ['purchase_comment','resolution1', 'resolution2', 'resolution3', 'resolution4', 'resolution5', 'resolution6', 'resolution7', 'resolution8']

    def form_valid(self, form):
        form.instance.purchase_rep = self.request.user #Inserts the author into the new post

        response = super().form_valid(form)  # Save the form data to the database

        if ('elevate' in self.request.POST) and (form.instance.form_status == 4): 
            form.instance.form_status += 2 #Increases the form status by 2

            pdf = blank_kgrns_render_pdf_view(self.request, pk=form.instance.id)

            prof = Supplier.objects.get(name=form.instance.supplier)
            emails = prof.email.values_list('email', flat=True)

            # Add PDF as attachment to each email
            subject = f'{form.instance.supplier} KGRN'
            message = f'Dear Sir/Madam,\n\nKindly find attached, your Goods’ Return Note number {form.instance.serial_num}.\n\nPlease contact us using the information provided below if you have any concerns, queries or need clarification.\n\n          Tel: +254 20 6420000\n          Email: purchase@kapa-oil.com\n\nThank you.'
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to = emails,
                cc= [config('BRIAN_EMAIL')],
                bcc = [config('BRIAN_EMAIL')],
                reply_to=[config('BRIAN_EMAIL')],
            )
            pdf_file = BytesIO(pdf.content)
            email.attach('report.pdf', pdf_file.getvalue(), 'application/pdf')
            email.send()

            messages.success(self.request, f'Form submitted and mail sent to {emails}')
            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 4):
            form.instance.form_status -= 3

            messages.success(self.request,'Form submitted!')
            return super().form_valid(form)
            
        else:
            return HttpResponse('Error')
        
        return response

class BlankKGRNPurchase2UpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_kgrn_item_purchase2.html'
    model = kgrn_item
    fields = ['pur_close_comment']

    def form_valid(self, form):
        profs = Profile.objects.filter(level='6')

        if ('elevate' in self.request.POST) and (form.instance.form_status == 6): 
            form.instance.form_status += 2 #Increases the form status by 2
            for prof in profs:
                email = EmailMessage(
                subject=f'{form.instance.department} department KGRN',
                body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been approved by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/items/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
                from_email=settings.EMAIL_HOST_USER,
                to=[prof.user.email],
                cc=[config('BRIAN_EMAIL')],
                reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
                )
                # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
                email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 6):
            form.instance.form_status -= 3
            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/items/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.hod.profile.email],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()

            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        else:
            return HttpResponse('Error : Form has already been approved or rejected')

class BlankCloseKGRNUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_kgrn_item_close.html'
    model = kgrn_item
    fields = ['accounts_comment']

    def form_valid(self, form):
        form.instance.closed_by = self.request.user
        if ('elevate' in self.request.POST) and (form.instance.form_status == 8): #If the button to elevate the form to the next level has been clicked
            form.instance.form_status += 2 #Increases the form status by 2

            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been closed by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/items/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.hod.profile.email, form.instance.author.profile.email],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],  # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        if ('elevate' in self.request.POST) and (form.instance.form_status == 5):
            form.instance.form_status += 3
            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been closed by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/items/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.hod.profile.email, form.instance.author.profile.email],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 8):
            form.instance.form_status -= 1

            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/items/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.hod.profile.email, form.instance.author.profile.email],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)
            
        if ('demote' in self.request.POST) and (form.instance.form_status == 7):
            form.instance.form_status -= 2

            email = EmailMessage(
            subject=f'{form.instance.department} department KGRN',
            body=f'KGRN number {form.instance.serial_num} submitted by {form.instance.author} has been rejected by {self.request.user}.\nKindly log on http://10.10.0.173:8000/waste/kgrns/items/ to view it.\nIn case of any challenges, feel free to contact IT for further assistance.',
            from_email=settings.EMAIL_HOST_USER,
            to=[form.instance.hod.profile.email, form.instance.author.profile.email],
            cc=[config('BRIAN_EMAIL')],
            reply_to=[config('BRIAN_EMAIL')],   # when the reply or reply all button is clicked, this is the reply to address, normally you don't have to set this if you want the receivers to reply to the from_email address
            )
            # email.content_subtype = 'html' # if the email body contains html tags, set this. Otherwise, omit it
            email.send()
            messages.success(self.request,'Form submitted and mail sent!')
            return super().form_valid(form)

        else:
            return HttpResponse('Error : Form has already been approved or rejected')



class GoodsIssueNoteCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    template_name = 'waste_management/raise_goodsissuenote.html'
    success_message = 'Form Submitted Successfully!'
    model = GoodsIssueNote
    form_class = GoodsIssueNoteForm
    success_url = reverse_lazy('gins')  # Replace 'success_url_name' with the URL name of the success page

    def form_valid(self, form):
        # Calculate total cost and total warehouse weight
        item_fields = ['material_1', 'material_2', 'material_3', 'material_4', 'material_5', 'material_6', 'material_7', 'material_8', 'material_9', 'material_10', 'material_11', 'material_12', 'material_13', 'material_14', 'material_15']
        weighbridge_weight_fields = ['weighbridge_weight_1', 'weighbridge_weight_2', 'weighbridge_weight_3', 'weighbridge_weight_4','weighbridge_weight_5', 'weighbridge_weight_6', 'weighbridge_weight_7', 'weighbridge_weight_8', 'weighbridge_weight_9',
                                    'weighbridge_weight_10', 'weighbridge_weight_11', 'weighbridge_weight_12', 'weighbridge_weight_13', 'weighbridge_weight_14', 'weighbridge_weight_15']
        qty_fields = ['material_quantity_1', 'material_quantity_2', 'material_quantity_3', 'material_quantity_4', 'material_quantity_5', 'material_quantity_6', 'material_quantity_7', 
                    'material_quantity_8', 'material_quantity_9', 'material_quantity_10', 'material_quantity_11', 'material_quantity_12', 'material_quantity_13', 'material_quantity_14', 'material_quantity_15']
        price_fields = ['material_1.price', 'material_2.price', 'material_3.price', 'material_4.price', 'material_5.price', 'material_6.price', 'material_7.price', 'material_8.price', 'material_9.price', 
                        'material_10.price', 'material_11.price', 'material_12.price', 'material_13.price', 'material_14.price', 'material_15.price']
        wh_weight_fields = ['warehouse_weight_1', 'warehouse_weight_2', 'warehouse_weight_3', 'warehouse_weight_4', 'warehouse_weight_5', 'warehouse_weight_6', 'warehouse_weight_7', 'warehouse_weight_8', 
                        'warehouse_weight_9', 'warehouse_weight_10', 'warehouse_weight_11', 'warehouse_weight_12', 'warehouse_weight_13', 'warehouse_weight_14', 'warehouse_weight_15']

        total_cost = 0
        total_wh_weight = 0

        for idx, item_field in enumerate(item_fields):
            item = getattr(form.instance, item_field)
            if item is not None:
                if getattr(form.instance, weighbridge_weight_fields[idx]) is not None:
                    total_cost += round(getattr(form.instance, weighbridge_weight_fields[idx]) * getattr(item, 'price'), 2)
                else:
                    total_cost += round(getattr(form.instance, qty_fields[idx]) * getattr(item, 'price'), 2)

                total_wh_weight += getattr(form.instance, wh_weight_fields[idx], 0)

        form.instance.gross_total = round(total_cost * int(1.16), 2)
        form.instance.my_total = total_cost
        form.instance.total_weight_wh = round(total_wh_weight, 2)

        # Set form_status based on isinternal
        form.instance.form_status = 2 if not form.instance.isinternal else 1

        # Set other fields
        form.instance.author = self.request.user
        form.instance.department_from = self.request.user.profile.department

        # Send emails to relevant users
        prev_serial_num = GoodsIssueNote.objects.count()
        serial_num = prev_serial_num + 1

        dept = self.request.user.profile.department_id
        profs = Profile.objects.filter(department=f'{dept}', level='2')

        for prof in profs:
            subject = 'Goods Issue Note'
            message = f'Hello {prof.user.first_name}, a new Goods Issue Note has been submitted by {form.instance.author} for your approval. Please login to the system on http://10.10.0.173:8000/waste/gins/ to view the form. \n The serial number is {serial_num}. \n To: {form.instance.department_to}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [config('BRIAN_EMAIL')]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

        return super().form_valid(form)

class HODGoodsIssueNoteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_hod_gin.html'
    model = GoodsIssueNote
    fields = ['hod_comment']

    def form_valid(self, form):
        form.instance.hod = self.request.user

        if ('elevate' in self.request.POST) and (form.instance.form_status == 2): #For internal forms, if the form is approved by the HOD, the form status is increased by 2
            form.instance.form_status += 2
            dept = form.instance.department_to
            profs = Profile.objects.filter(department=f'{dept}',level='2')

            for prof in profs:
                subject = 'Goods Issue Note'
                message = f'Hello {prof.user.first_name}, a Goods Issue Note has been submitted by {form.instance.hod} for your approval. Please login to the system on http://10.10.0.173:8000/waste/gins/ to view the form. \n  The serial number is {form.instance.id}. \n To: {form.instance.department_to}'
                email_from = settings.EMAIL_HOST_USER
                #recipient_list = [prof.user.email, config('BRIAN_EMAIL')]
                recipient_list = [config('BRIAN_EMAIL')]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return super().form_valid(form)

        if ('elevate' in self.request.POST) and (form.instance.form_status == 1): #For external forms, if the form is approved by the HOD, the form status is increased by 2
            form.instance.form_status += 2

            profs = Profile.objects.filter(level='7')

            for prof in profs:
                subject = 'Goods Issue Note'
                message = f'Hello {prof.user.first_name},\nA Goods Issue Note number {form.instance.id} has been submitted by {form.instance.hod} for your approval. Please login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form. \n Issued To: {form.instance.department_to}. \n Issued By: {form.instance.department_from}. \n Delivered by: {form.instance.delivered_by}. \n Net Value: {form.instance.my_total}'
                email_from = settings.EMAIL_HOST_USER
                #recipient_list = [prof.user.email, config('BRIAN_EMAIL')]
                recipient_list = [config('BRIAN_EMAIL')]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return super().form_valid(form)    


        if ('demote' in self.request.POST) and (form.instance.form_status == 2): #For internal forms, if the form is rejected by the HOD, the form status is decreased by 2
            form.instance.form_status -= 2
            author_name = form.instance.author.first_name
            author_email = form.instance.author.email

            subject = 'Goods Issue Note'
            message = f'Hello {author_name}, a Goods Issue Note number {form.instance.id} has been rejected by {form.instance.hod}. Please login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.\n To: {form.instance.department_to}'
            email_from = settings.EMAIL_HOST_USER
            #recipient_list = [author_email, config('BRIAN_EMAIL')]
            recipient_list = [config('BRIAN_EMAIL')]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 1): #For external forms, if the form is rejected by the HOD, the form status is decreased by 1
            form.instance.form_status -= 1 

            author_name = form.instance.author.first_name
            author_email = form.instance.author.email

            subject = 'Goods Issue Note'
            message = f'Hello {author_name}, a Goods Issue Note number {form.instance.id} has been rejected by {form.instance.hod}. Please login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.\n To: {form.instance.department_to}'
            email_from = settings.EMAIL_HOST_USER
            #recipient_list = [author_email, config('BRIAN_EMAIL')]
            recipient_list = [config('BRIAN_EMAIL')]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return super().form_valid(form)  

        else:
            return HttpResponse('Error : Form has already been approved or rejected')

class HODInternalGoodIssueNoteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_hod_gin_internal.html'
    model = GoodsIssueNote
    fields = ['department_internal','hod_comment']

    def form_valid(self, form):
        form.instance.hod = self.request.user

        if ('elevate' in self.request.POST) and (form.instance.form_status == 2): #For internal forms, if the form is approved by the HOD, the form status is increased by 2
            form.instance.form_status += 2
            dept = form.instance.department_internal_id
            profs = Profile.objects.filter(department=f'{dept}',level='2')

            for prof in profs:
                subject = 'Goods Issue Note'
                message = f'Hello {prof.user.first_name}, a Goods Issue Note has been submitted by {form.instance.hod} for your approval.\nPlease login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form. \n The serial number is {form.instance.id}. \n To: {form.instance.department_to}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [config('BRIAN_EMAIL')]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return super().form_valid(form)

        if ('elevate' in self.request.POST) and (form.instance.form_status == 1): #For external forms, if the form is approved by the HOD, the form status is increased by 2
            form.instance.form_status += 2

            profs = Profile.objects.filter(level='7')

            for prof in profs:
                subject = 'Goods Issue Note'
                message = f'Hello {prof.user.first_name},\nA Goods Issue Note has been submitted by {form.instance.hod} for your approval. \nPlease login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form. \n The serial number is {form.instance.id}. \n Issued To: {form.instance.department_to}. \n Issued By: {form.instance.department_from}. \n Net Value: {form.instance.my_total}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [prof.user.email, config('BRIAN_EMAIL')]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return super().form_valid(form)    


        if ('demote' in self.request.POST) and (form.instance.form_status == 2): #For internal forms, if the form is rejected by the HOD, the form status is decreased by 2
            form.instance.form_status -= 2
            author_name = form.instance.author.first_name
            author_email = form.instance.author.email

            subject = 'Goods Issue Note'
            message = f'Hello {author_name}, a Goods Issue Note number {form.instance.id} has been rejected by {form.instance.hod}. \nPlease login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.\n To: {form.instance.department_to}'
            email_from = settings.EMAIL_HOST_USER
            #recipient_list = [author_email, config('BRIAN_EMAIL')]
            recipient_list = [config('BRIAN_EMAIL')]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 1): #For external forms, if the form is rejected by the HOD, the form status is decreased by 1
            form.instance.form_status -= 1 

            author_name = form.instance.author.first_name
            author_email = form.instance.author.email

            subject = 'Goods Issue Note'
            message = f'Hello {author_name}, a Goods Issue Note number {form.instance.id} has been rejected by {form.instance.hod}. \nPlease login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.\n To: {form.instance.department_to}'
            email_from = settings.EMAIL_HOST_USER
            #recipient_list = [author_email, config('BRIAN_EMAIL')]
            recipient_list = [config('BRIAN_EMAIL')]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return super().form_valid(form)  

        else:
            return HttpResponse('Error: Form has already been approved or rejected')

class FMGoodsIssueNoteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/approve_goodsissuenote.html'
    model = GoodsIssueNote
    fields = ['fm_comment']

    # def get_context_data(self, **kwargs):
    #     context = {'my_variable': 0}
    #     return context

    def form_valid(self, form):
        form.instance.approved_by = self.request.user
        
        #print(form.instance.item_qty8)
        #print(form.instance.item_qty8_sale)

        if ('elevate' in self.request.POST) and (form.instance.form_status == 4): #No longer applicable ## For internal forms, if the form is approved by the FM, the form status is increased by 2
            form.instance.form_status += 2 

            return super().form_valid(form)

        if ('elevate' in self.request.POST) and (form.instance.form_status == 3): #For external forms, if the form is approved by the FM, the form status is increased by 2
            form.instance.form_status += 2 

            profs = Profile.objects.filter(level='13')
            profs2 = Profile.objects.filter(level='14')
            profs = profs | profs2
            print(profs)

            for prof in profs:
                subject = 'Goods Issue Note'
                message = f'Hello {prof.user.first_name},\nA Goods Issue Note submitted by {form.instance.department_from} has been approved by {form.instance.approved_by}. \nPlease login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.\n The serial number is {form.instance.id}. \n Issued To: {form.instance.department_to}. \n Issued By: {form.instance.department_from}. \n Net Value: {form.instance.my_total}'
                email_from = settings.EMAIL_HOST_USER
                #recipient_list = [prof.user.email, config('BRIAN_EMAIL')]
                recipient_list = [config('BRIAN_EMAIL')]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)


            return super().form_valid(form)    


        if ('demote' in self.request.POST) and (form.instance.form_status == 2): #No longer applicable ## For internal forms, if the form is rejected by the FM, the form status is decreased by 2
            form.instance.form_status -= 2 

            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 1): #For external forms, if the form is rejected by the FM, the form status is decreased by 1
            form.instance.form_status -= 1 

            author_name = form.instance.author.first_name
            author_email = form.instance.author.email

            dept = form.instance.author.profile.department_id
            profs = Profile.objects.filter(department=f'{dept}',level='2')

            for prof in profs:
                subject = 'Goods Issue Note'
                message = f'Hello {prof.user.first_name}, a Goods Issue Note number {form.instance.id} has been rejected by {form.instance.approved_by}. \nPlease login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.\n Issued To: {form.instance.department_to}'
                email_from = settings.EMAIL_HOST_USER
                #recipient_list = [prof.user.email, author_email, config('BRIAN_EMAIL')]
                recipient_list = [config('BRIAN_EMAIL')]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return super().form_valid(form)  

        else:
            return HttpResponse('Error: Form has already been approved or rejected')


class DepartmentRecieveGoodsIssueNoteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/dept_receivegoodsissuenote.html'
    model = GoodsIssueNote
    fields = ['received_by','dept_comment']

    def form_valid(self, form):
        form.instance.approved_by = self.request.user

        if ('elevate' in self.request.POST) and (form.instance.form_status == 4):
            form.instance.form_status += 4

            author_email = form.instance.author.email

            dept = form.instance.author.profile.department_id
            profs = Profile.objects.filter(department=f'{dept}',level='2')

            for prof in profs:
                subject = 'Goods Issue Note'
                message = f'Hello {prof.user.first_name}, Goods Issue Note number {form.instance.id} has been accepted by {form.instance.approved_by}. Please login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.\n Issued To: {form.instance.department_to}'
                email_from = settings.EMAIL_HOST_USER
                #recipient_list = [prof.user.email, author_email, config('BRIAN_EMAIL')]
                recipient_list = [config('BRIAN_EMAIL')]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return super().form_valid(form)

        if ('demote' in self.request.POST) and (form.instance.form_status == 4):
            form.instance.form_status -= 4 

            author_email = form.instance.author.email

            dept = form.instance.author.profile.department_id
            profs = Profile.objects.filter(department=f'{dept}',level='2')

            for prof in profs:
                subject = 'Goods Issue Note'
                message = f'Hello {prof.user.first_name}, Goods Issue Note number {form.instance.id} has been rejected by {form.instance.approved_by}. Please login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.\n Issued To: {form.instance.department_to}'
                email_from = settings.EMAIL_HOST_USER
                #recipient_list = [prof.user.email, author_email, config('BRIAN_EMAIL')]
                recipient_list = [config('BRIAN_EMAIL')]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)

            return super().form_valid(form)

        else:
            return HttpResponse('Error : Form has already been approved or rejected')

class SalesReceiveGoodsIssueNoteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'waste_management/sales_receivegoodsissuenote.html'
    model = GoodsIssueNote
    fields = ['weighbridge_weight_1', 'weighbridge_weight_2', 'weighbridge_weight_3', 'weighbridge_weight_4','weighbridge_weight_5', 'weighbridge_weight_6', 'weighbridge_weight_7', 'weighbridge_weight_8', 
            'weighbridge_weight_9','weighbridge_weight_10', 'weighbridge_weight_11', 'weighbridge_weight_12', 'weighbridge_weight_13', 'weighbridge_weight_14', 'weighbridge_weight_15', 'received_by', 'dept_comment', 'total_weight_wb']
    success_url = reverse_lazy('gins')  # Replace 'success_url_name' with the URL name of the success page

    def form_valid(self, form):
        # Calculate updated total price
        result = 0
        for idx in range(1, 16):
            item = getattr(form.instance, f'material_{idx}', None)
            qty_field = getattr(form.instance, f'weighbridge_weight_{idx}', None)
            if qty_field is None:
                qty_field = getattr(form.instance, f'material_quantity_{idx}', None)
            if item is not None:
                price = getattr(item, 'price', 0)
                result += round(qty_field * price, 2)

        form.instance.my_total = result
        form.instance.total_cost = round(result * int(1.16), 2)
        form.instance.received_by = str(self.request.user)

        if 'elevate' in self.request.POST and form.instance.form_status == 5:
            form.instance.form_status += 2
            self.send_approval_email(form.instance)
            return super().form_valid(form)

        if 'demote' in self.request.POST and form.instance.form_status == 5:
            form.instance.form_status -= 5
            self.send_rejection_email(form.instance)
            return super().form_valid(form)
        else:
            return HttpResponse('Error: Form has already been approved or rejected')

    def send_approval_email(self, instance):
        dept = instance.author.profile.department_id
        profs = Profile.objects.filter(department=f'{dept}', level='2')

        for prof in profs:
            subject = 'Goods Issue Note'
            message = f'Hello {prof.user.first_name}, Goods Issue Note number {instance.id} has been accepted by {instance.received_by}. Please login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.\n Issued To: {instance.department_to}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [config('BRIAN_EMAIL')]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

    def send_rejection_email(self, instance):
        dept = instance.author.profile.department_id
        profs = Profile.objects.filter(department=f'{dept}', level='2')

        for prof in profs:
            subject = 'Goods Issue Note'
            message = f'Hello {prof.user.first_name}, Goods Issue Note number {instance.id} has been rejected by {instance.received_by}. Please login to the system on http://10.10.0.173:8000/waste/dnotes/ to view the form.\n Issued To: {instance.department_to}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [config('BRIAN_EMAIL')]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)

class Goods_issue_note_ListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'goods_issue_notes'
    template_name = 'waste_management/gins.html'
    paginate_by: int = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = GoodsIssueNoteFilterSet(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        return GoodsIssueNote.objects.all()

