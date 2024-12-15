from django.shortcuts import render

def ai(request):
    return render(request, 'ai/ai.html')

def api_models(request):
    return render(request, 'ai/api_models/api_models.html')

def fine_tuning(request):
    return render(request, 'ai/fine_tuning/fine_tuning.html')

def fine_tuning_via_CPU(request):
    return render(request, 'ai/fine_tuning/fine_tuning_via_CPU.html')

def fine_tuning_via_CUDA(request):
    return render(request, 'ai/fine_tuning/fine_tuning_via_CUDA.html')

def fine_tuning_via_TPU(request):
    return render(request, 'ai/fine_tuning/fine_tuning_via_TPU.html')

def local_models(request):
    return render(request, 'ai/local_models/local_models.html')

def alibaba(request):
    return render(request, 'ai/local_models/alibaba.html')

def meta(request):
    return render(request, 'ai/local_models/meta.html')

def openai(request):
    return render(request, 'ai/local_models/openai.html')

def google(request):
    return render(request, 'ai/local_models/google.html')

def custom_models(request):
    return render(request, 'ai/local_models/custom_models.html')


