# Generated by Django 5.1.6 on 2025-02-20 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_userdetails_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='user_id',
            field=models.CharField(max_length=30, primary_key=True, serialize=False, unique=True),
        ),
    ]
