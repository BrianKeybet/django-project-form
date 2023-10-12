from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from rts_forms.models import Supplier
from django.urls import reverse
from simple_history.models import HistoricalRecords


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=40, blank=False)
    department_code = models.CharField(max_length=12, blank=False)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name 


class Material(models.Model):
    name = models.CharField(max_length=80, blank=False)
    material_code = models.CharField(max_length=12, blank=False)
    uom = models.CharField(max_length=20, null=True, blank=True, default='PC', verbose_name="UOM")
    price = models.DecimalField(max_digits=6, decimal_places=2, default = 0.00 , verbose_name="Net Price")
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=40, blank=False)
    customer_code = models.CharField(max_length = 40, blank = False, null = True)
    mobile_number1 = models.IntegerField(null=True, default='0')
    mobile_number2 = models.IntegerField(null=True, default='0')
    refered_by = models.CharField(max_length=40, blank=True, null=True)
    approved_by = models.CharField(max_length=40, blank=True, null=True)
    material1 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'item1', verbose_name = "Material Description")
    material2 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'item2', verbose_name = "Material Description")
    material3 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'item3', verbose_name = "Material Description")
    material4 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'item4', verbose_name = "Material Description")

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class waste_delivery_note(models.Model):
    date_posted = models.DateTimeField(default = timezone.now, verbose_name= "Date")
    department = models.CharField(max_length = 20, blank = True)
    form_status = models.IntegerField(null=True, default='0')
    author = models.ForeignKey(User, null = True, on_delete = models.PROTECT)
    hod = models.ForeignKey(User, null = True, on_delete = models.PROTECT, related_name = 'Head_of_Department', blank= True)
    warehouse_hod = models.ForeignKey(User, null = True, on_delete = models.PROTECT, related_name = 'Warehouse_Head_of_Department', blank= True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null = True, blank = True)
    waste_loader = models.CharField(max_length=20, null = True, blank = True, verbose_name = "Loaded By")
    #waste_offloader = models.CharField(max_length=20, null = True, blank = True, verbose_name = "Acknowledged By")
    waste_offloader = models.ForeignKey(User, null = True, blank = True, related_name = "Acknowledged_By", on_delete = models.PROTECT)
    item1 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material1', verbose_name = "Material Description")
    item_qty1 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item2 = models.ForeignKey(Material, on_delete = models.PROTECT,null = True, blank = True, related_name = 'material2', verbose_name = "Material Description")
    item_qty2 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item3 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material3', verbose_name = "Material Description")
    item_qty3 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item4 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material4', verbose_name = "Material Description")
    item_qty4 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item5 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material5', verbose_name = "Material Description")
    item_qty5 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item6 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material6', verbose_name = "Material Description")
    item_qty6 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item7 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material7', verbose_name = "Material Description")
    item_qty7 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item8 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material8', verbose_name = "Material Description")
    item_qty8 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    hod_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="HOD comment")
    warehouse_hod_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name=" Warehouse HOD Comment")
    checklist = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']   

    def get_absolute_url(self):
        return reverse('dnotes')


class Checklist(models.Model):
    
    form_serials = models.CharField(max_length = 100, blank = True) 
    date_posted = models.DateTimeField(default = timezone.now, verbose_name= "Date")
    author = models.ForeignKey(User, null = True, on_delete = models.PROTECT)
    checklist_status = models.IntegerField(null=True, default='0')

    class Meta:
        ordering = ['-id']

class Resolve(models.Model):
    name = models.CharField(max_length=40, blank=True)
    def __str__(self):
        return self.name

class Reason(models.Model):
    name = models.CharField(max_length=40, blank=True)
    def __str__(self):
        return self.name 

class kgrn(models.Model):
    serial_num = models.IntegerField(null=True, blank = True, unique=True)
    form_serials = models.CharField(max_length = 100, blank = True) 
    date_posted = models.DateTimeField(default = timezone.now, verbose_name= "Date")
    author = models.ForeignKey(User, null = True, on_delete = models.PROTECT)
    supplier = models.CharField(max_length = 100, blank = True)
    department = models.CharField(max_length = 100, blank = True)
    collected_by = models.CharField(max_length=20, null = True, blank = True, verbose_name = "Collected By")
    id_number = models.CharField(max_length = 20, blank = True, verbose_name = "ID Number")
    vehicle_no = models.CharField(max_length=20, null = True, blank = True, verbose_name = "Vehicle No")
    hod = models.ForeignKey(User, null = True, on_delete = models.PROTECT, related_name = 'H_O_D', blank= True)
    purchase_rep = models.ForeignKey(User, null = True, on_delete = models.PROTECT, related_name = 'Purchasing_Rep', blank= True)
    closed_by = models.ForeignKey(User, null = True, on_delete = models.PROTECT, related_name = 'Accounts_Rep', blank= True)
    hod_comment = models.CharField(max_length=100, null=True, blank=True,verbose_name="Head Of Dept comment")
    purchase_comment = models.CharField(max_length=100, null=True, blank=True,verbose_name="Purchase comment")
    pur_close_comment = models.CharField(max_length=100, null=True, blank=True,verbose_name="Purchase closing comment")
    accounts_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="Accounts comments")
    resolution = models.ForeignKey(Resolve, on_delete=models.PROTECT, null=True, blank = True, related_name = 'resolution', verbose_name = "Resolution")
    kgrn_status = models.IntegerField(null=True, default='0')

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('kgrns')

class kgrn_item(models.Model):
    serial_num = models.IntegerField(null=True, blank = True, unique=True)
    date_posted = models.DateTimeField(default = timezone.now, verbose_name= "Date")
    department = models.CharField(max_length = 20, blank = True)
    form_status = models.IntegerField(null=True, default='0')
    author = models.ForeignKey(User, null = True, on_delete = models.PROTECT)
    hod = models.ForeignKey(User, null = True, on_delete = models.PROTECT, related_name = 'Head_of_Dept', blank= True)
    purchase_rep = models.ForeignKey(User, null = True, on_delete = models.PROTECT, related_name = 'Purchasing_Representative', blank= True)
    pur_close_comment = models.CharField(max_length=100, null=True, blank=True,verbose_name="Procurement closing comment")
    closed_by = models.ForeignKey(User, null = True, on_delete = models.PROTECT, related_name = 'Accounts_Representative', blank= True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null = True, blank = True)
    waste_loader = models.CharField(max_length=20, null = True, blank = True, verbose_name = "Loaded By")
    collected_by = models.CharField(max_length=20, null = True, blank = True, verbose_name = "Collected By")
    id_number = models.CharField(max_length = 20, blank = True, verbose_name = "ID Number")
    vehicle_no = models.CharField(max_length=20, null = True, blank = True, verbose_name = "Vehicle No")
    item1 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material001', verbose_name = "Material Description")
    item_qty1 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    reason1 = models.ForeignKey(Reason, on_delete=models.PROTECT, null=True, blank = True, related_name = 'reason1', verbose_name = "")
    resolution1 = models.ForeignKey(Resolve, on_delete=models.PROTECT, null=True, related_name = 'resolution1', verbose_name = "")
    item2 = models.ForeignKey(Material, on_delete = models.PROTECT,null = True, blank = True, related_name = 'material002', verbose_name = "Material Description")
    item_qty2 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    reason2 = models.ForeignKey(Reason, on_delete=models.PROTECT, null=True, blank = True, related_name = 'reason2', verbose_name = "")
    resolution2 = models.ForeignKey(Resolve, on_delete=models.PROTECT, null=True, blank = True, related_name = 'resolution2', verbose_name = "")
    item3 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material003', verbose_name = "Material Description")
    item_qty3 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    reason3 = models.ForeignKey(Reason, on_delete=models.PROTECT, null=True, blank = True, related_name = 'reason3', verbose_name = "")
    resolution3 = models.ForeignKey(Resolve, on_delete=models.PROTECT, null=True, blank = True, related_name = 'resolution3', verbose_name = "")
    item4 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material004', verbose_name = "Material Description")
    item_qty4 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    reason4 = models.ForeignKey(Reason, on_delete=models.PROTECT, null=True, blank = True, related_name = 'reason4', verbose_name = "")
    resolution4 = models.ForeignKey(Resolve, on_delete=models.PROTECT, null=True, blank = True, related_name = 'resolution4', verbose_name = "")
    item5 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material005', verbose_name = "Material Description")
    item_qty5 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    reason5 = models.ForeignKey(Reason, on_delete=models.PROTECT, null=True, blank = True, related_name = 'reason5', verbose_name = "")
    resolution5 = models.ForeignKey(Resolve, on_delete=models.PROTECT, null=True, blank = True, related_name = 'resolution5', verbose_name = "")
    item6 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material006', verbose_name = "Material Description")
    item_qty6 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    reason6 = models.ForeignKey(Reason, on_delete=models.PROTECT, null=True, blank = True, related_name = 'reason6', verbose_name = "")
    resolution6 = models.ForeignKey(Resolve, on_delete=models.PROTECT, null=True, blank = True, related_name = 'resolution6', verbose_name = "")
    item7 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material007', verbose_name = "Material Description")
    item_qty7 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    reason7 = models.ForeignKey(Reason, on_delete=models.PROTECT, null=True, blank = True, related_name = 'reason7', verbose_name = "")
    resolution7 = models.ForeignKey(Resolve, on_delete=models.PROTECT, null=True, blank = True, related_name = 'resolution7', verbose_name = "")
    item8 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material008', verbose_name = "Material Description")
    item_qty8 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    reason8 = models.ForeignKey(Reason, on_delete=models.PROTECT, null=True, blank = True, related_name = 'reason8', verbose_name = "")
    resolution8 = models.ForeignKey(Resolve, on_delete=models.PROTECT, null=True, blank = True, related_name = 'resolution8', verbose_name = "")
    hod_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="HOD comment")
    purchase_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="Purchasing comment")
    accounts_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="Accounts comment")
    

    class Meta:
        ordering = ['-id']   

    def get_absolute_url(self):
        return reverse('kgrn_items')

class GoodsIssueNote(models.Model):
    date_posted = models.DateTimeField(default = timezone.now, verbose_name= "Date")
    department_from = models.CharField(max_length = 20, blank = True)
    department_to = models.ForeignKey(Customer, null = True, blank = True, related_name = "Department_to", on_delete = models.PROTECT)
    department_internal = models.ForeignKey(Department, on_delete = models.PROTECT, null = True, blank = True, related_name = 'Department_Internal')
    time_in = models.TimeField(auto_now=False, auto_now_add=False, blank = True, null = True)
    time_out = models.TimeField(auto_now=False, auto_now_add=False, blank = True, null = True)
    form_status = models.IntegerField(null=True, default='0')
    author = models.ForeignKey(User, null = True, on_delete = models.PROTECT)
    delivered_by = models.CharField(max_length=20, null = True, blank = True, verbose_name = "Delivered By")
    received_by = models.CharField(max_length=20, null = True, blank = True, verbose_name = "Received By")
    material_1 = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name='goods_issue_notes_1', verbose_name="Material 1 Description")
    material_quantity_1 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Material 1 Estimated Quantity")
    warehouse_weight_1 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Material 1 Warehouse Weight")
    weighbridge_weight_1 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="")
    material_2 = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True, related_name='goods_issue_notes_2', verbose_name="Material 2 Description")
    material_quantity_2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Material 2 Estimated Quantity")
    warehouse_weight_2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="Material 2 Warehouse Weight")
    weighbridge_weight_2 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="")
    material_3 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_3', verbose_name = "Material 3 Description")
    material_quantity_3 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 3 Estimated Quantity")
    warehouse_weight_3 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 3 Warehouse Weight")
    weighbridge_weight_3 =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_4 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_4', verbose_name = "Material 4 Description")
    material_quantity_4 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 4 Estimated Quantity")
    warehouse_weight_4 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 4 Warehouse Weight")
    weighbridge_weight_4 =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_5 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_5', verbose_name = "Material 5 Description")
    material_quantity_5 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 5 Estimated Quantity")
    warehouse_weight_5 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 5 Warehouse Weight")
    weighbridge_weight_5 =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_6 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_6', verbose_name = "Material 6 Description")
    material_quantity_6 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 6 Estimated Quantity")
    warehouse_weight_6 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 6 Warehouse Weight")
    weighbridge_weight_6 =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_7 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_7', verbose_name = "Material 7 Description")
    material_quantity_7 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 7 Estimated Quantity")
    warehouse_weight_7 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 7 Warehouse Weight")
    weighbridge_weight_7 =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_8 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_8', verbose_name = "Material 8 Description")
    material_quantity_8 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 8 Estimated Quantity")
    warehouse_weight_8 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 8 Warehouse Weight")
    weighbridge_weight_8= models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_9 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_9', verbose_name = "Material 9 Description")
    material_quantity_9 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 9 Estimated Quantity")
    warehouse_weight_9 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 9 Warehouse Weight")
    weighbridge_weight_9= models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_10 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_10', verbose_name = "Material 10 Description")
    material_quantity_10 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 10 Estimated Quantity")
    warehouse_weight_10 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 10 Warehouse Weight")
    weighbridge_weight_10= models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_11 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_11', verbose_name = "Material 11 Description")
    material_quantity_11 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 11 Estimated Quantity")
    warehouse_weight_11 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 11 Warehouse Weight")
    weighbridge_weight_11= models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_12 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_12', verbose_name = "Material 12 Description")
    material_quantity_12 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 12 Estimated Quantity")
    warehouse_weight_12 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 12 Warehouse Weight")
    weighbridge_weight_12= models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_13 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_13', verbose_name = "Material 13 Description")
    material_quantity_13 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 13 Estimated Quantity")
    warehouse_weight_13 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 13 Warehouse Weight")
    weighbridge_weight_13= models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_14 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_14', verbose_name = "Material 14 Description")
    material_quantity_14 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 14 Estimated Quantity")
    warehouse_weight_14 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 14 Warehouse Weight")
    weighbridge_weight_14= models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    material_15 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name='goods_issue_notes_15', verbose_name = "Material 15 Description")
    material_quantity_15 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 15 Estimated Quantity")
    warehouse_weight_15 = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name = "Material 15 Warehouse Weight")
    weighbridge_weight_15= models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    isinternal = models.BooleanField(default=False, verbose_name = "Internal/External")
    hod = models.ForeignKey(User, null = True, on_delete = models.PROTECT,  related_name = 'HOD', blank= True)
    hod_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="HOD comment")
    approved_by = models.ForeignKey(User, null = True, on_delete = models.PROTECT,  related_name = 'Approver', blank= True)
    fm_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="Comment")
    dept_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="Dept comment")
    my_total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Total")
    gross_total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Gross Total")
    total_weight_wh = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Total WH Weight")
    total_weight_wb = models.DecimalField(max_digits=15, decimal_places=2, blank=False, null=True, verbose_name="")

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('gins')