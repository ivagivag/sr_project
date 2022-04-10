# Generated by Django 4.0.3 on 2022-03-16 12:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0003_alter_product_stability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='assignee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tickets.product'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='severity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tickets.ticketsla'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tickets.ticketphase'),
        ),
        migrations.AlterField(
            model_name='ticketassessment',
            name='event_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticketassessment',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tickets.ticket'),
        ),
        migrations.AlterField(
            model_name='ticketeventlog',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticketeventlog',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tickets.ticket'),
        ),
        migrations.AlterField(
            model_name='ticketfiles',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tickets.ticket'),
        ),
        migrations.AlterField(
            model_name='ticketworkflow',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticketworkflow',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tickets.ticket'),
        ),
    ]