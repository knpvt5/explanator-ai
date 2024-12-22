from django.urls import path
from . import views

urlpatterns = [
    # path('', views.nvidia, name='nvidia'),
    
    path('nvidia-api-cb/', views.nvidia_api_cb, name='nvidia_api_cb'), 
        
    path('nvidia-api/', views.nvidia_api, name='nvidia_api'), 
    
    path('nvidia-docs-analyzer/', views.nvidia_docs_analyzer, name='nvidia_docs_analyzer'),
    path('nvidia-docs-analyzer-api/', views.nvidia_docs_analyzer_api, name='nvidia_docs_analyzer_api'),
    
    path('clear-uploaded-files-api/', views.clear_uploaded_files_api, name='clear_uploaded_files_api'),
    
]