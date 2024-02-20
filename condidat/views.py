
from django.shortcuts import render

from .models import UploadFileForm
def index(request):
        return render(request,"condidat.html")



def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return render(request,"condidat.html")
    else:
        form = UploadFileForm()
    return render(request, "upload.html")