# Generated by Django 4.2 on 2023-07-09 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0004_userinfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]