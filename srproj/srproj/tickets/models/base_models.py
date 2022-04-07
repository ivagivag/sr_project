from django.db import models


class TicketSla(models.Model):
    severity = models.CharField(max_length=30,)
    reaction_hours = models.PositiveSmallIntegerField()
    remark = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.severity}"

    class Mata:
        verbose_name_plural = 'Ticket sla'
