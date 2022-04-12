# Generated by Django 4.0.3 on 2022-04-12 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_account_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='accounts.company'),
        ),
    ]
