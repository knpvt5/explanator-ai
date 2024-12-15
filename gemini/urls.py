from django.urls import path
from . import views

urlpatterns = [
    path('', views.gemini, name='gemini'),
    path('gemini-api/', views.gemini_api, name='gemini_api'),
    path('gemini-api-chatbots/', views.gemini_api_chatbots, name='gemini_api_chatbots'),
    
    path('gemini-url-reader/', views.gemini_url_reader, name='gemini_url_reader'),
    path('gemini-url-reader-api/', views.gemini_url_reader_api, name='gemini_url_reader_api'),
    
    path('gemini-txt-reader/', views.gemini_txt_reader, name='gemini_txt_reader'),
    path('gemini-txt-reader-api/', views.gemini_txt_reader_api, name='gemini_txt_reader_api'),
    
    path('gemini-csv-reader/', views.gemini_csv_reader, name='gemini_csv_reader'),
    path('gemini-csv-reader-api/', views.gemini_csv_reader_api, name='gemini_csv_reader_api'),
    
    path('gemini-json-reader/', views.gemini_json_reader, name='gemini_json_reader'),
    path('gemini-json-reader-api/', views.gemini_json_reader_api, name='gemini_json_reader_api'),
    
    path('gemini-pdf-reader/', views.gemini_pdf_reader, name='gemini_pdf_reader'),
    path('gemini-pdf-reader-api/', views.gemini_pdf_reader_api, name='gemini_pdf_reader_api'),
]
