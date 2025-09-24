from django.shortcuts import render
# Create your views here.

def shark(request):
    return render(request, 'sharkinvest.html')