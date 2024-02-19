from django.db import models

class condidat(models.Model):

    nom=models.TextField(max_length=255)
    prenom=models.TextField(max_length=255)
    email=models.TextField(max_length=255)
    phone=models.TextField(max_length=255)
    login=models.TextField(max_length=255)
    password=models.TextField(max_length=255)
    entreprise=models.TextField(max_length=255)
    num_patent=models.IntegerField()
   