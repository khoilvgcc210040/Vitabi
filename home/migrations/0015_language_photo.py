# Generated by Django 4.2.7 on 2024-02-27 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_insurance_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='language_photos/'),
        ),
    ]