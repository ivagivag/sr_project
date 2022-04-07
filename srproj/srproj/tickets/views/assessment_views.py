from django.urls import reverse_lazy
from django.views import generic as views

from srproj.common.view_mixins import VerifyPermissionOwnMixin, CustomLoginRequiredMixin
from srproj.tickets.forms import TicketAssessmentForm
from srproj.tickets.models.core_models import Ticket, TicketAssessment


class AssessmentCreateView(CustomLoginRequiredMixin, VerifyPermissionOwnMixin, views.CreateView):
    model = TicketAssessment
    ticket_model = Ticket
    form_class = TicketAssessmentForm
    template_name = 'ticket_assessment/create_assessment.html'
    required_perm = 'assess tickets'

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