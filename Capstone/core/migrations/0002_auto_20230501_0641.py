# Generated by Django 3.0.9 on 2023-05-01 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='feeback',
            new_name='feedback',
        ),
    ]