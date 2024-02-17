
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("Login",include("Login.urls")),
    path("Admin",include("Admin.urls")),
    path("condidat",include("condidat.urls")),
    path("recruteur",include("recruteur.urls")),

]
