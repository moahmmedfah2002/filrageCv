from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Recruteur(models.Model):
    email = models.TextField(max_length=255)
    nom = models.TextField(max_length=100)
    prenom = models.TextField(max_length=100)
    telephone = models.TextField(max_length=15)
    entreprise = models.TextField(max_length=100)
    numero_patent = models.TextField(max_length=100)
    password= models.TextField(max_length=100)
   





class Condidat(models.Model):
    email = models.TextField(max_length=255)
    nom = models.TextField(max_length=100)
    prenom = models.TextField(max_length=100)
    tel = models.TextField(max_length=10)
    password = models.TextField(max_length=100)
   

    