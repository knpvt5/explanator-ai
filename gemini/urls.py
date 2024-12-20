from django.urls import path
from . import views

urlpatterns = [
    path('', views.gemini, name='gemini'),
    
    path('gemini-api/', views.gemini_api, name='gemini_api'),
    path('gemini-api-cb/', views.gemini_api_cb, name='gemini_api_cb'),
    
    path('gemini-docs-analyzer/', views.gemini_docs_analyzer, name='gemini_docs_analyzer'),
    path('gemini-docs-analyzer-api/', views.gemini_docs_analyzer_api, name='gemini_docs_analyzer_api'),
    
    
]
