from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from rts_forms.models import Supplier
from django.urls import reverse

import computed_property

# Create your models here.

class Material(models.Model):
    name = models.CharField(max_length=80, blank=False)
    material_code = models.CharField(max_length=12, blank=False)
    uom = models.CharField(max_length=20, null=True, blank=True, default='PC', verbose_name="UOM")
    price = models.DecimalField(max_digits=6, decimal_places=2, default = 0.00 , verbose_name="Price")

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
    #id = models.AutoField(primary_key=True)
    date_posted = models.DateTimeField(default = timezone.now, verbose_name= "Date")
    department_from = models.CharField(max_length = 20, blank = True)
    department_to = models.CharField(max_length = 20, blank = True)
    form_status = models.IntegerField(null=True, default='0')
    author = models.ForeignKey(User, null = True, on_delete = models.PROTECT)
    delivered_by = models.CharField(max_length=20, null = True, blank = True, verbose_name = "Delivered By")
    received_by = models.ForeignKey(User, null = True, blank = True, related_name = "Received_By", on_delete = models.PROTECT)
    item1 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material01', verbose_name = "Material Description")
    item_qty1 = models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty1_sale =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    item2 = models.ForeignKey(Material, on_delete = models.PROTECT,null = True, blank = True, related_name = 'material02', verbose_name = "Material Description")
    item_qty2 = models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty2_sale =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    item3 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material03', verbose_name = "Material Description")
    item_qty3 = models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty3_sale =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    item4 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material04', verbose_name = "Material Description")
    item_qty4 = models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty4_sale =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    item5 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material05', verbose_name = "Material Description")
    item_qty5 = models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty5_sale =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    item6 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material06', verbose_name = "Material Description")
    item_qty6 = models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty6_sale =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    item7 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material07', verbose_name = "Material Description")
    item_qty7 = models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty7_sale =models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    item8 = models.ForeignKey(Material, on_delete = models.PROTECT, null = True, blank = True, related_name = 'material08', verbose_name = "Material Description")
    item_qty8 = models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "Estimated Quantity")
    item_qty8_sale = models.DecimalField(max_digits=15, decimal_places=2, null = True, blank = True, verbose_name = "")
    isInternal = models.BooleanField(default=False, verbose_name = "Internal/External")
    approved_by = models.ForeignKey(User, null = True, on_delete = models.PROTECT,  related_name = 'Approver', blank= True)
    fm_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="FM comment")
    dept_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="Dept comment")
    my_total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="Total")

    # my_total = computed_property.ComputedFloatField(compute_from='get_cost', null=True, default='0', verbose_name="Total")

    # #https://django-computed-property.readthedocs.io/en/latest/
    # @property
    # def get_cost(self, *args, **kwargs):
    #     if self.item1 != None:
    #         if self.item_qty1_sale != None:
    #             i1 = round(self.item_qty1_sale * float(self.item1.price), 2)
    #         else:
    #             i1 = round(self.item_qty1 * float(self.item1.price), 2)
    #     else:
    #         i1 = 0
    #     if self.item2 != None:
    #         if self.item_qty2_sale != None:
    #             i2 = round(self.item_qty2_sale * float(self.item2.price), 2)
    #         else:
    #             i2 = round(self.item_qty2 * float(self.item2.price), 2)
    #     else:
    #         i2 = 0
    #     if self.item3 != None:
    #         if self.item_qty3_sale != None:
    #             i3 = round(self.item_qty3_sale * float(self.item3.price), 2)
    #         else:
    #             i3 = round(self.item_qty3 * float(self.item3.price), 2)
    #     else:
    #         i3 = 0
    #     if self.item4 != None:
    #         if self.item_qty4_sale != None:
    #             i4 = round(self.item_qty4_sale * float(self.item4.price), 2)
    #         else:
    #             i4 = round(self.item_qty4 * float(self.item4.price), 2)
    #     else:   
    #         i4 = 0
    #     if self.item5 != None:
    #         if self.item_qty5_sale != None:
    #             i5 = round(self.item_qty5_sale * float(self.item5.price), 2)
    #         else:
    #             i5 = round(self.item_qty5 * float(self.item5.price), 2)
    #     else:
    #         i5 = 0
    #     if self.item6 != None:
    #         if self.item_qty6_sale != None:
    #             i6 = round(self.item_qty6_sale * float(self.item6.price), 2)
    #         else:
    #             i6 = round(self.item_qty6 * float(self.item6.price), 2)
    #     else:
    #         i6 = 0
    #     if self.item7 != None:
    #         if self.item_qty7_sale != None:
    #             i7 = round(self.item_qty7_sale * float(self.item7.price), 2)
    #         else:
    #             i7 = round(self.item_qty7 * float(self.item7.price), 2)
    #     else:
    #         i7 = 0
    #     if self.item8 != None:
    #         if self.item_qty8_sale != None:
    #             i8 = round(self.item_qty8_sale * float(self.item8.price), 2)
    #         else:
    #             i8 = round(self.item_qty8 * float(self.item8.price), 2)
    #     else:
    #         i8 = 0
 
    #     result = round(i1 + i2 + i3 + i4 + i5 + i6 + i7 + i8, 2)
    #     #return f'{result:n}'
    #     return result

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('gins')