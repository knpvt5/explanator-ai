from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai, name='ai'),
    # path('ai/', views.ai, name='ai'), 
        
    path('chatbots/', views.chatbots, name='chatbots'), 
    
    path('docs-analyzer/', views.docs_analyzer, name='docs_analyzer'), 
    
    path('fine-tuning/', views.fine_tuning, name='fine_tuning'),

    path('fine-tuning-via-CPU/', views.fine_tuning_via_CPU, name='fine_tuning_via_CPU'), 
    
    path('fine-tuning-via-CUDA/', views.fine_tuning_via_CUDA, name='fine_tuning_via_CUDA'),
    
    path('fine-tuning-via-TPU/', views.fine_tuning_via_TPU, name='fine_tuning_via_TPU'), 
    
    path('local-models/', views.local_models, name='local_models'), 
    
    path('alibaba/', views.alibaba, name='alibaba'), 
    
    path('meta/', views.meta, name='meta'), 
    
    path('openai/', views.openai, name='openai'), 
    
    path('google/', views.google, name='google'), 
    
    path('custom-models/', views.custom_models, name='custom_models'), 
]