# Generated by Django 4.2.11 on 2024-05-08 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
