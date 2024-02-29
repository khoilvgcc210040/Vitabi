# Generated by Django 4.2.7 on 2024-02-12 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_answer_odds_less_than_1_answer_odds_more_than_1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='odds_less_than_1',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='odds_more_than_1',
        ),
        migrations.CreateModel(
            name='Conclusion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('odds_condition', models.CharField(choices=[('>=1', 'Odds >= 1'), ('<1', 'Odds < 1')], max_length=10)),
                ('answers', models.ManyToManyField(related_name='conclusions', to='home.answer')),
            ],
        ),
    ]
