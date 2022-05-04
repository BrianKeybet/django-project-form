from django.urls import path
from .views import FormsDetailView, FormsHODUpdateView, FormsQAOUpdateView, FormsFMUpdateView, FormsPrintView
from . import views

urlpatterns = [
    path('', views.home, name='forms-home'),
    path('rts/', views.RTSForm.as_view(), name='rts'),
    path('rtsforms/', views.FormsView.as_view(), name='rtsforms'),
    path('rtsform/<int:pk>/', FormsDetailView.as_view(), name='rtsform-detail'),
    path('rtsform/<int:pk>/update/', FormsHODUpdateView.as_view(), name='rtsform-update'),
    path('rtsform/<int:pk>/update1/', FormsQAOUpdateView.as_view(), name='rtsform-update1'),
    path('rtsform/<int:pk>/update2/', FormsFMUpdateView.as_view(), name='rtsform-update2'),

    path('rtsform/<int:pk>/print/', FormsPrintView.as_view(), name='rtsform-print'),
    path('rtsform/pdf/<pk>', views.rtsforms_render_pdf_view, name='rtsform_pdf_view'),


    path('rtsform/<int:pk>/update/elevate', views.elevate_form_status, name='elevate-status'),
    path('rtsform/<int:pk>/update/demote', views.demote_form_status, name='demote-status'),

    path('rtsform/photo/<pk>', views.get_material_image, name='get_photo'),
]