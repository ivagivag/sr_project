# Generated by Django 4.0.3 on 2022-03-16 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='end_of_life',
            new_name='end_of_support',
        ),
    ]
