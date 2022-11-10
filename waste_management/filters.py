import django_filters
from .models import goods_issue_note

class goods_issue_noteFilter(django_filters.FilterSet):
    #author__name = django_filters.CharFilter(lookup_expr='icontains')
    #department_to__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = goods_issue_note
        fields = ['id','author', 'department_to', 'form_status']