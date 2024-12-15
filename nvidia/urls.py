from django.urls import path
from . import views

urlpatterns = [
    path('', views.nvidia, name='nvidia'),
    path('nvidia-api-chatbots/', views.nvidia_api_chatbots, name='nvidia_api_chatbots'), 
    path('nvidia-api/', views.nvidia_api, name='nvidia_api'), 
    
    path('nvidia-url-reader/', views.nvidia_url_reader, name='nvidia_url_reader'),
    path('nvidia-url-reader-api/', views.nvidia_url_reader_api, name='nvidia_url_reader_api'),  
    
    path('nvidia-txt-reader/', views.nvidia_txt_reader, name='nvidia_txt_reader'),
    path('nvidia-txt-reader-api/', views.nvidia_txt_reader_api, name='nvidia_txt_reader_api'),
    
    path('nvidia-csv-reader/', views.nvidia_csv_reader, name='nvidia_csv_reader'),
    path('nvidia-csv-reader-api/', views.nvidia_csv_reader_api, name='nvidia_csv_reader_api'),
    
    path('nvidia-json-reader/', views.nvidia_json_reader, name='nvidia_json_reader'),
    path('nvidia-json-reader-api/', views.nvidia_json_reader_api, name='nvidia_json_reader_api'),
    
    path('nvidia-pdf-reader/', views.nvidia_pdf_reader, name='nvidia_pdf_reader'),
    path('nvidia-pdf-reader-api/', views.nvidia_pdf_reader_api, name='nvidia_pdf_reader_api'),
]