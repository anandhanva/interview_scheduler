# Generated by Django 5.1.6 on 2025-02-20 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='user_mail',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
    ]
