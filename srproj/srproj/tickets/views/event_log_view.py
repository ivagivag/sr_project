from django.views import generic as views

from srproj.common.view_mixins import VerifyPermissionOwnMixin, CustomLoginRequiredMixin
from srproj.tickets.models.core_models import Ticket, TicketWorkFlow, TicketEventLog


class TicketEventLogView(CustomLoginRequiredMixin, VerifyPermissionOwnMixin, views.ListView):
    model = TicketEventLog
    ticket_model = Ticket
    template_name = 'tickets/event_log_ticket.html'
    context_object_name = 'log_events'
    required_perm = 'event log'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tid'] = self.kwargs['tid']

        return context

    def get_queryset(self):
        query_set = super().get_queryset()

        return query_set.filter(ticket=self.kwargs['tid']).order_by('event_time')
