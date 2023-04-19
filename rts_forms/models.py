from django.db import models
from django.urls import reverse
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=40, blank=False)
    def __str__(self):
        return self.name

class EmailAddress(models.Model):
    email = models.EmailField(max_length=254, blank=False)
    def __str__(self):
        return self.email

class Supplier(models.Model):
    name = models.CharField(max_length=40, blank=False)
    supplier_code = models.CharField(max_length = 40, blank = False, null = True)
    email = models.ManyToManyField(EmailAddress)
    
    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=40, blank=False)
    material_code = models.CharField(max_length=12, blank=False)
    uom = models.CharField(max_length=20, null=True, blank=True, default='PC', verbose_name="UOM")

    class Meta:
        ordering = ['name'] 

    def __str__(self):
        return self.name 

class Reason(models.Model):
    name = models.CharField(max_length=40, blank=False)
    def __str__(self):
        return self.name

class Resolution(models.Model):
    name = models.CharField(max_length=40, blank=True)
    def __str__(self):
        return self.name                               



class RTSform(models.Model):
    date_posted = models.DateTimeField(default=timezone.now, verbose_name="Date")
    author = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    department = models.CharField(max_length=20, blank=False, default='Warehouse')
    department_internal = models.ForeignKey(Department, on_delete = models.PROTECT, null = True, blank = True, related_name = 'Department_Affected')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    vehicle_number = models.CharField(max_length=40, verbose_name="Vehicle Number")
    dnote_number = models.CharField(max_length=40, verbose_name="D/Note number")
    dnote_date = models.DateField(verbose_name="D/Note Date")
    material_description = models.ForeignKey(Material, on_delete=models.PROTECT, verbose_name="Material description")
    quality_issue = models.CharField(max_length=100, verbose_name="Quality issue")
    reason_for_rejection = models.ForeignKey(Reason, on_delete=models.PROTECT, verbose_name="Reason for rejection")
    delivery_quantity = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name="Delivery quantity")
    sampled_quantity = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True,  verbose_name="Sampled quantity")
    quantity_affected = models.DecimalField(max_digits=8, decimal_places=2, null = True, blank = True, verbose_name="Quantity affected")
    acceptable_level = models.CharField(max_length=40, verbose_name="Acceptable level")
    batches_sampled= models.CharField(max_length=40, verbose_name="Batches sampled")
    mould = models.CharField(max_length=40, verbose_name="Mould")
    hod_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="HOD comment")
    image = models.ImageField(upload_to='rts_pics', default='default.jpg', null=True, blank=True, verbose_name="Picture")
    form_status = models.IntegerField(null=True, default='0')
    qao_comment = models.CharField(max_length=100, null=True, blank=True, verbose_name="QAO comment")
    resolution = models.ForeignKey(Resolution, on_delete=models.PROTECT, null=True)

    class Meta:
        ordering = ['-id']      
    
    def __str__(self):
        return f'Form Serial: {self.id}'

    def elevate_status(self):
        self.form_status += 2 

    def demote_status(self):
        self.form_status -= 1

    def get_absolute_url(self):
        return reverse('rtsforms')     
