# Generated by Django 4.2.17 on 2024-12-08 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_habit_completedhabit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='completedhabit',
            name='completed_date',
            field=models.DateField(),
        ),
    ]
