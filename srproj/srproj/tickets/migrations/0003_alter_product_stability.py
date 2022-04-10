# Generated by Django 4.0.3 on 2022-03-16 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_rename_end_of_life_product_end_of_support'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stability',
            field=models.CharField(choices=[('PRE ALPHA', 'PRE ALPHA'), ('ALPHA', 'ALPHA'), ('BETA', 'BETA'), ('RELEASE CANDIDATE', 'RELEASE CANDIDATE'), ('STABLE RELEASE', 'STABLE RELEASE'), ('END OF SUPPORT', 'END OF SUPPORT')], max_length=17),
        ),
    ]