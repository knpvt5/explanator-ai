from django.urls import path
from . import views

urlpatterns = [
    path('', views.nvidia, name='nvidia'),
    path('nvidia-api-chatbots/', views.nvidia_api_chatbots, name='nvidia_api_chatbots'), 
    path('nvidia-api/', views.nvidia_api, name='nvidia_api'), 
    
    path('nvidia-docs-analyzer/', views.nvidia_docs_analyzer, name='nvidia_docs_analyzer'),
    path('nvidia-docs-analyzer-api/', views.nvidia_docs_analyzer_api, name='nvidia_docs_analyzer_api'),
    
    path('nvidia-url-reader/', views.nvidia_url_reader, name='nvidia_url_reader'),
    path('nvidia-url-reader-api/', views.nvidia_url_reader_api, name='nvidia_url_reader_api'),  
]