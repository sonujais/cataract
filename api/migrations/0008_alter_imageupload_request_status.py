# Generated by Django 5.1.1 on 2024-09-25 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_recommendationrequest_disease_predict'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageupload',
            name='request_status',
            field=models.CharField(choices=[('none', 'None'), ('requested', 'Requested'), ('reviewed', 'Reviewed')], default='none', max_length=20),
        ),
    ]
