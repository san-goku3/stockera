from django.shortcuts import render

# Create your views here.
def brokercompare(request):
    return render(request, 'brokercompare.html')