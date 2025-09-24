from django.shortcuts import render

# Create your views here.
def brokers(request):
    return render(request, 'brokers.html')