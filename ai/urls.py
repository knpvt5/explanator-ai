from django.urls import path
from . import views

urlpatterns = [
    # path('', views.ai, name='ai'),
    # path('ai/', views.ai, name='ai'), 
                

    path('about-us/', views.about_us, name='about_us'),
    
    path('contact-us/', views.contact_us, name='contact_us'),
    
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),
     
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