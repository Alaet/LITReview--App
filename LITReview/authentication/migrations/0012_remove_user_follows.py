# Generated by Django 4.0.2 on 2022-02-21 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_userfollow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='follows',
        ),
    ]
