# Generated by Django 5.1.1 on 2024-09-21 13:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authen', '0001_initial'),
        ('user', '0003_delete_eyeimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='available_slots', to='authen.doctorprofile')),
            ],
        ),
    ]
