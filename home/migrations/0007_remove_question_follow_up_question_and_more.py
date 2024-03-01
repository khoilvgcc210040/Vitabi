# Generated by Django 4.2.7 on 2024-02-12 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_remove_patient_id_alter_patient_user_question_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='follow_up_question',
        ),
        migrations.AddField(
            model_name='question',
            name='is_first_question',
            field=models.BooleanField(default=False, help_text='Chọn để đặt câu hỏi này là câu hỏi đầu tiên.'),
        ),
    ]