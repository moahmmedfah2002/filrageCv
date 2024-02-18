from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

def login(request):
    return render(request,"Login.html")

def logup(request):
    return render(request,"logup.html")