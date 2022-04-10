# Generated by Django 4.0.3 on 2022-03-19 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0010_rename_owner_ticketworkflow_creator_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticketassessment',
            old_name='event_creator',
            new_name='creator',
        ),
        migrations.AlterField(
            model_name='ticketassessment',
            name='overall',
            field=models.CharField(choices=[('Excellent', 'Excellent'), ('Very Good', 'Very Good'), ('Poor', 'Poor'), ('Good', 'Good'), ('Fair', 'Fair')], max_length=9),
        ),
        migrations.AlterField(
            model_name='ticketassessment',
            name='reaction',
            field=models.CharField(choices=[('Excellent', 'Excellent'), ('Very Good', 'Very Good'), ('Poor', 'Poor'), ('Good', 'Good'), ('Fair', 'Fair')], max_length=9),
        ),
        migrations.AlterField(
            model_name='ticketassessment',
            name='resolve',
            field=models.CharField(choices=[('Excellent', 'Excellent'), ('Very Good', 'Very Good'), ('Poor', 'Poor'), ('Good', 'Good'), ('Fair', 'Fair')], max_length=9),
        ),
    ]