# Generated by Django 4.1.7 on 2024-02-18 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0002_rename_condidat_candidate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Candidate',
            new_name='condidat',
        ),
    ]