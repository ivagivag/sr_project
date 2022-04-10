# Generated by Django 4.0.3 on 2022-03-17 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_alter_ticket_assignee_alter_ticket_creator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfamily',
            name='domain',
            field=models.CharField(choices=[('Access', 'Access'), ('IP', 'IP'), ('Mobile', 'Mobile'), ('Power', 'Power'), ('Transmission', 'Transmission')], default='IP', max_length=12),
            preserve_default=False,
        ),
    ]