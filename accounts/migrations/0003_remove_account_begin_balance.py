# Generated by Django 4.2.6 on 2023-10-25 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='begin_balance',
        ),
    ]
