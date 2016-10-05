from django.shortcuts import render
from django.http import HttpResponse

def print_code(request):
    return render(request, 'print_code.html')

def print_webpage(request):
    return render(request, 'print_webpage.html')
