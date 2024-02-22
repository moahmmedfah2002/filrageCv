from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from autoslug import AutoSlugField
from django_countries.fields import CountryField


CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Internship', 'Internship'),
    ('Remote', 'Remote'),
)


class Profile(models.Model):
     user = models.OneToOneField(
         User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
     full_name = models.CharField(max_length=200, null=True, blank=True)
     country = CountryField(null=True, blank=True)
     location = models.CharField(max_length=255, null=True, blank=True)
     resume = models.FileField(upload_to='resumes', null=True, blank=True)
     grad_year = models.IntegerField(blank=True)
     looking_for = models.CharField(
         max_length=30, choices=CHOICES, default='Full Time', null=True)
     slug = AutoSlugField(populate_from='user', unique=True)

     def get_absolute_url(self):
         return "/profile/{}".format(self.slug)

     def save(self, *args, **kwargs):
         super().save(*args, **kwargs)

     def __str__(self):
         return self.user.username


class Skill(models.Model):
     skill = models.CharField(max_length=200)
     user = models.ForeignKey(
         User, related_name='skills', on_delete=models.CASCADE)


class SavedJobs(models.Model):
    idoffre=models.IntegerField()
    idcandidat =models.IntegerField() 