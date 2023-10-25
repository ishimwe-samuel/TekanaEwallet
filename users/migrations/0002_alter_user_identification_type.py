# Generated by Django 4.2.6 on 2023-10-25 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='identification_type',
            field=models.CharField(choices=[('NID', 'Nation ID'), ('PSP', 'Passport')], default='NID', max_length=3),
        ),
    ]
