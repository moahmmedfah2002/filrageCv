# Generated by Django 5.0.2 on 2024-02-17 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='condidat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.TextField(max_length=255)),
                ('prenom', models.TextField(max_length=255)),
                ('email', models.TextField(max_length=255)),
                ('phone', models.TextField(max_length=255)),
                ('login', models.TextField(max_length=255)),
                ('password', models.TextField(max_length=255)),
                ('entreprise', models.TextField(max_length=255)),
                ('num_patent', models.IntegerField()),
            ],
        ),
    ]
