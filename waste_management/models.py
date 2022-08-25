from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from rts_forms.models import Supplier
from django.urls import reverse

# Create your models here.

class Material(models.Model):
    name = models.CharField(max_length=80, blank=False)
    material_code = models.CharField(max_length=12, blank=False)

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


class checklist(models.Model):
    
    form_serials = models.CharField(max_length = 100, blank = True) 
    date_posted = models.DateTimeField(default = timezone.now, verbose_name= "Date")
    author = models.ForeignKey(User, null = True, on_delete = models.PROTECT)
    checklist_status = models.IntegerField(null=True, default='0')

    class Meta:
        ordering = ['-id']

class kgrn(models.Model):
    
    form_serials = models.CharField(max_length = 100, blank = True) 
    date_posted = models.DateTimeField(default = timezone.now, verbose_name= "Date")
    author = models.ForeignKey(User, null = True, on_delete = models.PROTECT)
    kgrn_status = models.IntegerField(null=True, default='0')

    class Meta:
        ordering = ['-id']

class goods_issue_note(models.Model):
    date_posted = models.DateTimeField(default = timezone.now, verbose_name= "Date")
    department_from = models.CharField(max_length = 20, blank = True)
    department_to = models.CharField(max_length = 20, blank = True)
    form_status = models.IntegerField(null=True, default='0')
    author = models.ForeignKey(User, null = True, on_delete = models.PROTECT)
    delivered_by = models.CharField(max_length=20, null = True, blank = True, verbose_name = "Delivered By")
    received_by = models.ForeignKey(User, null = True, blank = True, related_name = "Received_By", on_delete = models.PROTECT)
    item1 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material01', verbose_name = "Material Description")
    item_qty1 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty1_sale = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Sales Estimated Quantity")
    item2 = models.ForeignKey(Material, on_delete = models.PROTECT,null = True, blank = True, related_name = 'material02', verbose_name = "Material Description")
    item_qty2 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty2_sale = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Sales Estimated Quantity")
    item3 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material03', verbose_name = "Material Description")
    item_qty3 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty3_sale = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Sales Estimated Quantity")
    item4 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material04', verbose_name = "Material Description")
    item_qty4 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty4_sale = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Sales Estimated Quantity")
    item5 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material05', verbose_name = "Material Description")
    item_qty5 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty5_sale = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Sales Estimated Quantity")
    item6 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material06', verbose_name = "Material Description")
    item_qty6 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty6_sale = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Sales Estimated Quantity")
    item7 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material07', verbose_name = "Material Description")
    item_qty7 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty7_sale = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Sales Estimated Quantity")
    item8 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material08', verbose_name = "Material Description")
    item_qty8 = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty8_sale = models.FloatField(max_length = 40, null = True, blank = True, verbose_name = "Sales Estimated Quantity")
    isInternal = models.BooleanField(default=False, verbose_name = "Internal/External")
    approved_by = models.ForeignKey(User, null = True, on_delete = models.PROTECT,  related_name = 'Approved_by', blank= True)
    fm_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="FM comment")
    dept_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="Dept comment")

    class Meta:
        ordering = ['-id']   

    def get_absolute_url(self):
        return reverse('gins')