import django_filters
from .models import *
from django.forms.widgets import TextInput, Select


class goods_issue_noteFilter(django_filters.FilterSet):

    CHOICES = (
        ('0','Rejected'),
        ('1','Submitted to HOD (Internal)'),
        ('2','Submitted to HOD (External)'),
        ('3','Submitted to FM/Directors'),
        ('4','Submitted to Department'),
        ('5','Submitted to sales'),
        ('7','Complete (Internal)'),
        ('8','Complete (External)'),
    )
    status = django_filters.ChoiceFilter(label='Status', choices=CHOICES, method='check_status')
    #status = django_filters.ChoiceFilter(label='Status', choices=CHOICES, method='check_status', widget=Select(attrs={'placeholder': 'FORM STATUS'}))
    #Date_posted = django_filters.IsoDateTimeFilter(label='Date Posted', field_name='date_posted', lookup_expr='gte')

    class Meta:
        model = goods_issue_note
        fields = {
            'id': ['exact'],
            'author': ['exact'],
            'department_from': ['icontains'],
            #'form_status': ['icontains'],
        }

    def check_status(self, queryset, name, value):
        return queryset.filter(form_status__exact=value)

class waste_delivery_noteFilter(django_filters.FilterSet):
    
        CHOICES = (
            ('1','Rejected by HOD'),
            ('2','Submitted to HOD'),
            ('3','Rejected by Warehouse'),
            ('4','Approved by HOD'),
            ('5','Submitted to sales'),
            ('6','Submitted to Warehouse Clerk'),
            ('8','Submitted to Warehouse HOD'),
            ('10','Delivery note ready'),
            ('11','Delivery note ready'),
        )
        status = django_filters.ChoiceFilter(label='Status', choices=CHOICES, method='check_status')
        #Date_posted = django_filters.IsoDateTimeFilter(label='Date Posted', field_name='date_posted', lookup_expr='gte')
    
        class Meta:
            model = waste_delivery_note
            fields = {
                'id': ['exact'],
                'author': ['exact'],
                'department': ['icontains'],
                'supplier': ['exact'],
                #'form_status': ['icontains'],
            }
    
        def check_status(self, queryset, name, value):
            return queryset.filter(form_status__exact=value)

class ChecklistFilter(django_filters.FilterSet):
    
        class Meta:
            model = waste_delivery_note
            fields = {
                'id': ['exact'],
                'author': ['exact'],
            }
    
        def check_status(self, queryset, name, value):
            return queryset.filter(form_status__exact=value)


class kgrn_itemFilter(django_filters.FilterSet):
    
        CHOICES = (
            ('1','Rejected by HOD'),
            ('2','Submitted to  Dept HOD'),
            ('3','Rejected by Procurement'),
            ('4','Submitted to Purchasing'),
            ('6','Awaiting Supplier Action'),
            ('8','Submitted to accounts'),
            ('10','Closed'),
        )
        status = django_filters.ChoiceFilter(label='Status', choices=CHOICES, method='check_status')
        #Date_posted = django_filters.IsoDateTimeFilter(label='Date Posted', field_name='date_posted', lookup_expr='gte')
    
        class Meta:
            model = kgrn_item
            fields = {
                'id': ['exact'],
                'author': ['exact'],
                'department': ['icontains'],
                'supplier': ['exact'],
            }
    
        def check_status(self, queryset, name, value):
            return queryset.filter(form_status__exact=value)

class kgrnFilter(django_filters.FilterSet):
    
        CHOICES = (
            ('0','Add Driver Details'),
            ('15','Submitted to Dept HOD'),
            ('1','Rejected by HOD'),
            ('2','Submitted to Purchasing'),
            ('3','Rejected by Purchasing'),
            ('4','Awaiting Supplier Action'),
            ('6','Submitted to accounts'),
            ('8','Closed'),
        )
        status = django_filters.ChoiceFilter(label='Status', choices=CHOICES, method='check_status')
        #Date_posted = django_filters.IsoDateTimeFilter(label='Date Posted', field_name='date_posted', lookup_expr='gte')
    
        class Meta:
            model = kgrn
            fields = {
                'serial_num': ['exact'],
                'author': ['exact'],
                'department': ['icontains'],
            }
    
        def check_status(self, queryset, name, value):
            return queryset.filter(kgrn_status__exact=value)
