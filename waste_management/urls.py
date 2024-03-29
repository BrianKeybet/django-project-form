from django.urls import path
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
    path('dnoteskgrn/', views.Dnotes_KGRN_ListView.as_view(), name='dnotes_kgrn'),
    path('kgrn/new/', views.BlankKGRN_CreateView.as_view(), name='blank_kgrn-create'),
    path('bkgrn/<int:pk>/update/', views.BlankKGRNHODUpdateView.as_view(), name='bkgrn-update'),
    path('bkgrn/<int:pk>/update1/', views.BlankKGRNPurchaseUpdateView.as_view(), name='bkgrn-update1'),
    path('bkgrn/<int:pk>/updatec1/', views.BlankKGRNPurchase2UpdateView.as_view(), name='bkgrn-updatec1'),
    path('bkgrn/<int:pk>/update2/', views.BlankCloseKGRNUpdateView.as_view(), name='bkgrn-update2'),
    path('bkgrn/pdf/<pk>', views.blank_kgrns_render_pdf_view, name='bkgrn_pdf_view'),
    path('kgrns/items/', views.KGRN_ItemsListView.as_view(), name='kgrn_items'),
    path('dnoteskgrn/kgrn', views.create_kgrn, name='create_kgrn'),
    path('kgrn/<int:pk>/update0/', views.KGRNStocksUpdateView.as_view(), name='kgrn-update0'),
    path('kgrn/<int:pk>/update/', views.KGRNHODUpdateView.as_view(), name='kgrn-update'),
    path('kgrn/<int:pk>/update1/', views.KGRNPurchaseUpdateView.as_view(), name='kgrn-update1'),
    path('kgrn/<int:pk>/updatec1/', views.KGRNPurchase2UpdateView.as_view(), name='kgrn-updatec1'),
    path('kgrn/<int:pk>/update2/', views.CloseKGRNUpdateView.as_view(), name='kgrn-update2'),
    path('kgrn/pdf/<pk>', views.kgrns_render_pdf_view, name='kgrn_pdf_view'),
    path('kgrns/', views.KGRNListView.as_view(), name='kgrns'),
    path('newIssueNote/', views.GoodsIssueNoteCreateView.as_view(), name='goods_issue_note-create'),
    path('gins/', views.Goods_issue_note_ListView.as_view(), name='gins'),
    path('IssueNote/<int:pk>/hodupdate/', views.HODGoodsIssueNoteUpdateView.as_view(), name='goods_issue_note-hodupdate'),
    path('IssueNote/<int:pk>/hodupdate1/', views.HODInternalGoodIssueNoteUpdateView.as_view(), name='goods_issue_note-hodupdate1'),
    path('IssueNote/<int:pk>/update/', views.FMGoodsIssueNoteUpdateView.as_view(), name='goods_issue_note-update'),
    path('IssueNote/<int:pk>/update1/', views.DepartmentRecieveGoodsIssueNoteUpdateView.as_view(), name='goods_issue_note-update1'),
    path('IssueNote/<int:pk>/update2/', views.SalesReceiveGoodsIssueNoteUpdateView.as_view(), name='goods_issue_note-update2'),
    path('IssueNote/pdf/<pk>', views.goods_issue_note_render_pdf_view, name='goods_issue_note_pdf_view'), 
    path('IssueNote/pdf1/<pk>', views.goods_issue_note_external_render_pdf_view, name='goods_issue_note_pdf_view1'),    
]