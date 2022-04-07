from django.urls import reverse_lazy
from django.views import generic as views

from srproj.common.view_mixins import CustomLoginRequiredMixin, VerifyPermissionChangeOwnMixin
from srproj.tickets.forms import EntryRegistrationForm
from srproj.tickets.models.core_models import Ticket, TicketWorkFlow


class EntryCreateView(CustomLoginRequiredMixin, VerifyPermissionChangeOwnMixin, views.CreateView):
    model = TicketWorkFlow
    ticket_model = Ticket
    form_class = EntryRegistrationForm
    template_name = 'ticket_entry/create_entry.html'
    required_perm = 'create entry'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tid'] = self.kwargs['tid']
        context['ticket'] = Ticket.objects.get(pk=self.kwargs['tid'])
        return context

    def form_valid(self, form):
        form.instance.ticket = Ticket.objects.get(pk=self.kwargs['tid'])
        form.instance.creator = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ticket details', kwargs={'pk': self.kwargs['tid']})
