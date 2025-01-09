from django.urls import path
from . import views
from .view import nvidia_api_datasets_views
from .view import gemini_api_datasets_views

urlpatterns = [
    # path('', views.data_sets, name='data_sets'),
        
    path('tokenized-datasets/', views.tokenized_datasets, name='tokenized_datasets'), 
    
    path('non-tokenized-datasets/', views.non_tokenized_datasets, name='non_tokenized_datasets'),
    
    path('nvidia-api-prompt-generator-ds/', nvidia_api_datasets_views.nvidia_api_prompt_generator_ds, name='nvidia_api_prompt_generator_ds'),
    path('nvidia-api-prompt-generator-ds-api/', nvidia_api_datasets_views.nvidia_api_prompt_generator_ds_api, name='nvidia_api_prompt_generator_ds_api'),

    path('gemini-api-prompt-generator-ds/', gemini_api_datasets_views.gemini_api_prompt_generator_ds, name='gemini_api_prompt_generator_ds'),
    path('gemini-api-prompt-generator-ds-api/', gemini_api_datasets_views.gemini_api_prompt_generator_ds_api, name='gemini_api_prompt_generator_ds_api'),
    
    
    path('nvidia-raw-dataset-reader/', nvidia_api_datasets_views.nvidia_raw_dataset_reader, name='nvidia_raw_dataset_reader'),
    path('nvidia-raw-dataset-reader-api/', nvidia_api_datasets_views.nvidia_raw_dataset_reader_api, name='nvidia_raw_dataset_reader_api'),
    
    path('gemini-raw-dataset-reader/', gemini_api_datasets_views.gemini_raw_dataset_reader, name='gemini_raw_dataset_reader'),
    path('gemini-raw-dataset-reader-api/', gemini_api_datasets_views.gemini_raw_dataset_reader_api, name='gemini_raw_dataset_reader_api'),
    
]