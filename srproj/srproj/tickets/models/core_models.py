from django.contrib.auth import get_user_model
from django.db import models

from srproj.settings import TIME_ZONE
from srproj.tickets.models.base_models import TicketSla
from srproj.tickets.models.suppl_models import Product
from datetime import datetime
import pytz

bg_tz = pytz.timezone(TIME_ZONE)
UserModel = get_user_model()


class Ticket(models.Model):
    OPEN = "Open"
    ASSIGNED = "Assigned"
    IN_PROCESS = "In Process"
    SOLUTION_PROVIDED = "Solution Provided"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    STATE_CHOICES = [(x, x) for x in (OPEN, ASSIGNED, IN_PROCESS, SOLUTION_PROVIDED, RESOLVED, CLOSED)]
    RESTRICTED_CHOICES = [(x, x) for x in (IN_PROCESS, SOLUTION_PROVIDED, RESOLVED)]

    summary = models.CharField(max_length=255,)
    description = models.TextField()
    product = models.ForeignKey(
        Product,
        on_delete=models.RESTRICT,
    )
    creator = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
        related_name='creator',
    )
    assignee = models.ForeignKey(
        get_user_model(),
        on_delete=models.RESTRICT,
        related_name='assignee',
        null=True,
        blank=True,
    )
    modifier = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
        related_name='modifier',
    )
    severity = models.ForeignKey(
        TicketSla,
        on_delete=models.RESTRICT,
    )
    state = models.CharField(
        max_length=max([len(x) for (_, x) in STATE_CHOICES]),
        choices=STATE_CHOICES,
    )
    register_date = models.DateTimeField()
    resolve_date = models.DateTimeField(
        null=True,
        blank=True,
    )
    resolve_due_date = models.DateTimeField()
    rating = models.CharField(
        max_length=30,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
    )

    @property
    def is_delayed(self):
        if self.is_active:
            result = self.resolve_due_date <= datetime.now()
        else:
            result = self.resolve_due_date < self.resolve_date
        return result

    @property
    def delay(self):
        if self.is_active:
            result = datetime.now() - self.resolve_due_date
        else:
            result = self.resolve_date - self.resolve_due_date
        return result if result.total_seconds() > 0 else None

    def __str__(self):
        return f"#{self.id} Summary: {self.summary}"
        # return f"{self.id} {self.summary} {self.severity} {self.state} {self.creator} {self.assignee}"


class TicketWorkFlow(models.Model):
    NOTE = "Note"
    RCA = "RCA"
    CORRECTIVE_ACTION = "Corrective Action"
    RESOLUTION = "Resolution"
    TYP_CHOICES = [(x, x) for x in (NOTE, RCA, CORRECTIVE_ACTION, RESOLUTION)]

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.RESTRICT,
    )
    note = models.TextField(
        verbose_name="SR Note"
    )
    typ = models.CharField(
        max_length=max([len(x) for (_, x) in TYP_CHOICES]),
        choices=TYP_CHOICES,
        verbose_name="Type:"
    )
    event_time = models.DateTimeField(auto_now_add=True,)
    creator = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.ticket_id} {self.ticket.summary} {self.creator}"


class TicketEventLog(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
    )
    event = models.CharField(max_length=300,)
    creator = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )
    event_time = models.DateTimeField()

    def __str__(self):
        return f"SR#{self.ticket_id} event by {self.creator} on {self.event_time}"
        # return f"{self.ticket_id} {self.ticket.summary} {self.event} {self.creator}"


class TicketAssessment(models.Model):
    POOR = "Poor"
    FAIR = "Fair"
    GOOD = "Good"
    VERY_GOOD = "Very Good"
    EXCELLENT = "Excellent"
    CHOICES = [(x, x) for x in (EXCELLENT, VERY_GOOD, GOOD, POOR, FAIR)]
    CHOICE_MAX_LEN = max([len(y) for (x, y) in CHOICES])
    NEGATIVE_CHOICES = (POOR, FAIR)
    POSITIVE_CHOICES = (GOOD, VERY_GOOD, EXCELLENT)

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
    )
    reaction = models.CharField(
        max_length=CHOICE_MAX_LEN,
        choices=CHOICES,
        verbose_name="Please, evaluate the SR reaction time:",
    )
    reaction_remark = models.TextField(
        null=True,
        blank=True,
    )
    resolve = models.CharField(
        max_length=CHOICE_MAX_LEN,
        choices=CHOICES,
        verbose_name="Please, evaluate the SR resolution:",
    )
    resolve_remark = models.TextField(
        null=True,
        blank=True,
    )
    overall = models.CharField(
        max_length=CHOICE_MAX_LEN,
        choices=CHOICES,
    )
    overall_remark = models.TextField(
        null=True,
        blank=True,
        verbose_name="Please, evaluate the overall support:",
    )
    creator = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )
    event_time = models.DateTimeField(auto_now_add=True,)

    @property
    def is_negative(self):
        return self.reaction in self.NEGATIVE_CHOICES \
            or self.resolve in self.NEGATIVE_CHOICES \
            or self.overall in self.NEGATIVE_CHOICES

    def __str__(self):
        return f"{self.ticket_id} {self.ticket.summary} {self.reaction} {self.resolve} {self.overall}"

    class Meta:
        ordering = ('-event_time', )
