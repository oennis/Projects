# Generated by Django 3.0.9 on 2023-05-01 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_book_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='user',
        ),
    ]
