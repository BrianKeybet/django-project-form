from django.db import models
from django.urls import reverse
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User

#Belonging to another application
class Speaker(models.Model):
    name = models.CharField(max_length=40, blank=False)
    def __str__(self):
        return self.name

class Track(models.Model):
    title = models.CharField(max_length=40, blank=False)
    def __str__(self):
        return self.title

class Department(models.Model):
    name = models.CharField(max_length=40, blank=False)
    def __str__(self):
        return self.name  

class Supplier(models.Model):
    name = models.CharField(max_length=40, blank=False)
    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=40, blank=False)
    material_code = models.CharField(max_length=12, blank=False)
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

class Presentation(models.Model):
    title = models.CharField(max_length=40, blank=False)
    abstract = models.TextField(blank=False)
    track = models.ForeignKey(Track, on_delete=models.PROTECT)
    speaker = models.ForeignKey(Speaker, on_delete=models.PROTECT)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk}) 

#Sealing choices
my_choices = [('G','Good'),('L','Leaking')]

class BPinspectionform(models.Model):
    boolean = models.BooleanField(default=False, verbose_name="New Inspection Form")
    date_posted = models.DateTimeField(default=timezone.now)
    serial_number = models.CharField(max_length=40)
    sample1 = models.CharField(max_length=40, blank=False)
    sample2 = models.CharField(max_length=40, blank=False)
    sample3 = models.CharField(max_length=40, blank=False)
    sample4 = models.CharField(max_length=40, blank=False)
    sample5 = models.CharField(max_length=40, blank=False)

    
    S1Sealing=models.CharField(max_length=40, choices=my_choices)
    S2Sealing=models.CharField(max_length=40, choices=my_choices)
    S3Sealing=models.CharField(max_length=40, choices=my_choices)
    S4Sealing=models.CharField(max_length=40, choices=my_choices)
    S5Sealing=models.CharField(max_length=40, choices=my_choices)
    #S5Sealing=models.CharField(label='Sealing', widget=forms.RadioSelect(choices=CHOICES))

    def __str__(self):
        return self.serial_number

    class Meta:
        ordering = ['id'] 

class RTSform(models.Model):
    date_posted = models.DateTimeField(default=timezone.now, verbose_name="Date")
    author = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    department = models.CharField(max_length=20, blank=False, default='Warehouse')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    vehicle_number = models.CharField(max_length=40, verbose_name="Vehicle Number")
    dnote_number = models.CharField(max_length=40, verbose_name="D/Note number")
    dnote_date = models.CharField(max_length=40, verbose_name="D/Note Date")
    material_description = models.ForeignKey(Material, on_delete=models.PROTECT, verbose_name="Material description")
    quality_issue = models.CharField(max_length=40, verbose_name="Quality issue")
    reason_for_rejection = models.ForeignKey(Reason, on_delete=models.PROTECT, verbose_name="Reason for rejection")
    delivery_quantity = models.CharField(max_length=40, verbose_name="Delivery quantity")
    sampled_quantity = models.CharField(max_length=40, verbose_name="Sampled quantity")
    quantity_affected = models.CharField(max_length=40, verbose_name="Quantity affected")
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
