from django.db import models

class condidat(models.Model):

    nom=models.TextField(max_length=255)
    prenom=models.TextField(max_length=255)
    email=models.TextField(max_length=255)
    phone=models.TextField(max_length=255)
    password=models.TextField(max_length=255)
    entreprise=models.TextField(max_length=255)
    num_patent=models.IntegerField()

class Recruteur(models.Model):
    id_recruteur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    entreprise = models.CharField(max_length=255)
    num_patent = models.CharField(max_length=255, blank=True, null=True)
    clef_recruteur = models.CharField(max_length=255, blank=True, null=True)
    
# Create and save multiple instances
recruteur1 = Recruteur(
    nom='Smith',
    prenom='John',
    email='john.smith@example.com',
    phone='123456789',
    login='john_smith',
    password='hashed_password',
    entreprise='ABC Corp',
    num_patent='P12345',
    clef_recruteur='abc123'
)
recruteur1.save()

recruteur2 = Recruteur(
    nom='Doe',
    prenom='Jane',
    email='jane.doe@example.com',
    phone='987654321',
    login='jane_doe',
    password='hashed_password',
    entreprise='XYZ Ltd',
    num_patent='P67890',
    clef_recruteur='xyz789'
)
recruteur2.save()