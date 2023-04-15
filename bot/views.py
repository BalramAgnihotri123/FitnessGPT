from django.shortcuts import render
from django.http import HttpResponse
from . import utils

def chatbot(request):
    
    if request.method == 'POST':
        return HttpResponse("Hello")

    return render(request, "bot/index.html")