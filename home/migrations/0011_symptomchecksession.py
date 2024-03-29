# Generated by Django 4.2.7 on 2024-02-25 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0010_remove_answer_odds_less_than_1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SymptomCheckSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('conclusion_text', models.TextField()),
                ('odds_percentage', models.JSONField(default=dict)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='symptom_sessions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
