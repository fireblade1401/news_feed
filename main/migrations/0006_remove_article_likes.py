# Generated by Django 4.2.4 on 2023-09-04 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='likes',
        ),
    ]
