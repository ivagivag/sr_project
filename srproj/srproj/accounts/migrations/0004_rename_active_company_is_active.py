# Generated by Django 4.0.3 on 2022-03-25 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_company_alter_accountprofile_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='active',
            new_name='is_active',
        ),
    ]