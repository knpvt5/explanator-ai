from django.shortcuts import render

# Create your views here.
def datasets(request):
    return render(request, 'datasets/datasets.html')

def tokenized_datasets(request):
    return render(request, 'datasets/tokenized_datasets.html')

def non_tokenized_datasets(request):
    return render(request, 'datasets/non_tokenized_datasets.html')


