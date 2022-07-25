from django.urls import path
from .views import waste_delivery_noteCreateView
from . import views

urlpatterns = [
    path('new/', views.waste_delivery_noteCreateView.as_view(), name='waste_delivery_note-create'),
    path('dnote/<int:pk>/update/', views.DnoteHODUpdateView.as_view(), name='dnote-update'),
    path('dnote/<int:pk>/update1/', views.DnoteWHUpdateView.as_view(), name='dnote-update1'),
    path('dnotes/', views.DnotesListView.as_view(), name='dnotes'),
    path('dnote/pdf/<pk>', views.dnotes_render_pdf_view, name='dnote_pdf_view'),
    path('check/checklist', views.create_checklist, name='create_checklist'),
    path('accept/checklist', views.accept_checklist, name='accept_checklist'),
    path('checklists/', views.CheckListView.as_view(), name='checklists'),
    path('checklists/pdf/<pk>', views.checklists_render_pdf_view, name='checklist_pdf_view'),
]