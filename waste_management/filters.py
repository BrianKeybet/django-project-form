import django_filters
from .models import *


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
    #Date_posted = django_filters.IsoDateTimeFilter(label='Date Posted', field_name='date_posted', lookup_expr='gte')

    class Meta:
        model = goods_issue_note
        fields = {
            'id': ['exact'],
            'author': ['exact'],
            'department_to': ['exact'],
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
