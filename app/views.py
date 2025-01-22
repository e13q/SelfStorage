from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')

def boxes(request):
    return render(request,'boxes.html')

def rent(request):
    return render(request,'my-rent.html')