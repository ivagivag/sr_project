from django.db.models.signals import post_save
from django.dispatch import receiver
from srproj.tickets.models.core_models import Ticket, TicketWorkFlow, TicketEventLog, TicketAssessment
from srproj.common.helpers import calc_assess
from datetime import datetime


def time_format(field):
    return field.strftime("%d-%m-%Y, %H:%M") if field else None


@receiver(post_save, sender=Ticket)
def create_ticket_log(sender, instance, created, **kwargs):
    action = "New ticket created" if created else "Modified"

    ticket_log = TicketEventLog(
        ticket=instance,
        creator=instance.modifier,
        event=f"Action: <{action}> Ticket ID: <{instance.id}> Summary: <{instance.summary}> "
              f"Product: <{instance.product}> Severity: <{instance.severity}> "
              f"State: <{instance.state}> Expected resolve date: <{time_format(instance.resolve_due_date)}> " 
              f"Resolve date: <{time_format(instance.resolve_date)}> " 
              f"Creator: <{instance.creator}> Assignee: <{instance.assignee}> "
              f"Action executed by: <{instance.modifier}> Active: <{instance.is_active}>",
        event_time=datetime.now()
    )
    ticket_log.save()


@receiver(post_save, sender=TicketWorkFlow)
def create_ticket_log(sender, instance, created, **kwargs):
    ticket_log = TicketEventLog(
        ticket=instance.ticket,
        creator=instance.creator,
        event=f"Action: <New entry created> Entry ID: <{instance.id}> "
              f"Note: <{instance.note}> "
              f"Type: <{instance.typ}> Action executed by: <{instance.creator}>",
        event_time=datetime.now()
    )
    ticket_log.save()


# @receiver(post_save, sender=TicketAssessment)
# def create_ticket_log(sender, instance, created, **kwargs):
#     ticket_log = TicketEventLog(
#         ticket=instance.ticket,
#         creator=instance.creator,
#         event=f"Action: <New assessment created> Assessment ID: <{instance.id}> "
#               f"Support reaction time: <{instance.reaction}> Ticket resolution: <{instance.resolve}> "
#               f"Overall experience: <{instance.overall}> Action executed by: <{instance.creator}>",
#         event_time=datetime.now()
#     )
#     ticket_log.save()


@receiver(post_save, sender=TicketAssessment)
def create_ticket_log_and_calc_ticket_assessment(sender, instance, created, **kwargs):
    ticket_log = TicketEventLog(
        ticket=instance.ticket,
        creator=instance.creator,
        event=f"Action: <New assessment created> Assessment ID: <{instance.id}> "
              f"Support reaction time: <{instance.reaction}> Ticket resolution: <{instance.resolve}> "
              f"Overall experience: <{instance.overall}> Action executed by: <{instance.creator}>",
        event_time=datetime.now()
    )
    ticket_log.save()

    all_assess_rows = sender.objects.filter(ticket=instance.ticket)
    rows_to_calc = [(x.reaction, x.resolve, x.overall) for x in all_assess_rows]
    ticket = Ticket.objects.get(pk=instance.ticket_id)
    result = calc_assess(rows_to_calc)
    ticket.rating = result
    ticket.save()
