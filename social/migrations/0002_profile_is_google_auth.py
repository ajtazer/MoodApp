# Generated by Django 4.2 on 2023-07-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_google_auth',
            field=models.BooleanField(default=False),
        ),
    ]