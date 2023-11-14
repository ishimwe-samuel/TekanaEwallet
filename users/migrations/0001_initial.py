# Generated by Django 4.2.6 on 2023-11-14 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('identification_type', models.CharField(choices=[('NID', 'Nation ID'), ('PSP', 'Passport')], default='NID', max_length=3)),
                ('identification', models.CharField(blank=True, max_length=100, null=True)),
                ('dob', models.DateField(null=True)),
                ('active', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('is_suspended', models.BooleanField(default=False)),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAdditionalInfo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('country', models.CharField(blank=True, max_length=10, null=True)),
                ('city', models.CharField(blank=True, max_length=10, null=True)),
                ('province', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number1', models.CharField(max_length=15, unique=True)),
                ('phone_number2', models.CharField(max_length=15, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='information', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=6, unique=True)),
                ('otp_type', models.CharField(max_length=5)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verification_codes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
