# Generated by Django 5.1.3 on 2024-11-15 20:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('frequency', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], default='daily', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.user')),
            ],
        ),
        migrations.CreateModel(
            name='CompletedHabit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_date', models.DateField(auto_now_add=True)),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.habit')),
            ],
        ),
    ]
