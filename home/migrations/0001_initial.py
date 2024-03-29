# Generated by Django 4.2.7 on 2024-02-05 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import home.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('website_link', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_patient', models.BooleanField(default=True)),
                ('fullname', models.CharField(max_length=50)),
                ('gender', models.BooleanField()),
                ('dob', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('nationality', models.CharField(max_length=40)),
                ('language', models.CharField(max_length=20)),
                ('height', models.IntegerField(default=0)),
                ('weight', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('opening_time', models.TimeField(default=home.models.Hospital.get_current_time)),
                ('closing_time', models.TimeField(default=home.models.Hospital.get_current_time)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=20)),
                ('supported_insurance', models.ManyToManyField(to='home.insurance')),
                ('supported_languages', models.ManyToManyField(to='home.language')),
            ],
        ),
    ]
