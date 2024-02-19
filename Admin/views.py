from django.shortcuts import render
from django.http import HttpRequest,HttpResponse

def index(request):
    return render(request,"admin-home.html")
def candidate(request):
    return render(request,"candidate.html")
    