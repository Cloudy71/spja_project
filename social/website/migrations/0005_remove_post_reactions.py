# Generated by Django 2.1.3 on 2018-12-07 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20181206_1927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='reactions',
        ),
    ]
