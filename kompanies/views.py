from django.shortcuts import render
from archive.models import BusinessLine  

def home(request):

    business_lines = BusinessLine.objects.all()

    context = {
        'business_lines': business_lines  
    }

    # Context ile beraber 'index.html' şablonunu render ediyoruz
    return render(request, 'index.html', context)
