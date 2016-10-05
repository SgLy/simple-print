from django.shortcuts import render
from django.http import HttpResponse

def print_code(request):
    return HttpResponse('Code printing page')

# Create your views here.
