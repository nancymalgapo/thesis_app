from django.conf.urls import url

from . import views

urlpatterns =[
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^user/$', views.user_home, name='user_home'),
    url(r'^user_scan/$', views.user_home_scan, name='user_home_scan'),
    url(r'^directupload/$', views.user_upload_direct, name='user_upload_direct'),
    url(r'^user_procedure_flatbed/$', views.user_procedure_flatbed, name='user_procedure_flatbed'),
    url(r'^user_procedure_feeder/$', views.user_procedure_feeder, name='user_procedure_feeder'),
    url(r'^doc_info_feeder/$', views.doc_info_feeder, name='doc_info_feeder'),
    url(r'^doc_info_flatbed/$', views.doc_info_flatbed, name='doc_info_flatbed'),
    url(r'^scan_upload_feeder/$', views.user_upload_scan_feeder, name='user_upload_scan_feeder'),
    url(r'^scan_upload_flatbed/$', views.user_upload_scan_flatbed, name='user_upload_scan_flatbed'),
    url(r'^result/$', views.doc_result, name='doc_result'),
    url(r'^error_page/$', views.error_page, name='error_page'),
    
    url(r'^doc_list/$', views.document_list, name='doc_list'),
    url(r'^document/$', views.document, name='document'),
    url(r'^document_check/$', views.document_check, name='document_check'),
]