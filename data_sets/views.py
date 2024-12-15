from django.shortcuts import render

# Create your views here.
def datasets(request):
    return render(request, 'data_sets/datasets.html')

def tokenized_datasets(request):
    return render(request, 'data_sets/tokenized_datasets.html')

def non_tokenized_datasets(request):
    return render(request, 'data_sets/non_tokenized_datasets.html')


