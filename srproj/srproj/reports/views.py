from django.views import generic as views

from srproj.common.view_mixins import VerifyPermissionMixin, CustomLoginRequiredMixin
from srproj.tickets.models.core_models import TicketAssessment, Ticket


class TicketAssessmentFiltered(CustomLoginRequiredMixin, VerifyPermissionMixin, views.ListView):
    model = TicketAssessment
    template_name = 'reports/customer_feedback.html'
    context_object_name = 'assessments'
    required_perm = 'feedback'
    paginate_by = 4

    def get_queryset(self):
        """
        get_queryset preferred rather than get_context_data as it executes before the pagination takes place
        """
        queryset = self.model.objects.all()
        if self.kwargs['fb'] == 'negative':
            queryset = [x for x in queryset if x.is_negative]
        elif self.kwargs['fb'] == 'positive':
            queryset = [x for x in queryset if not x.is_negative]
        else:
            queryset = []
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fb'] = self.kwargs['fb']

        return context


class TicketViolatedSla(CustomLoginRequiredMixin, VerifyPermissionMixin, views.ListView):
    model = Ticket
    template_name = 'reports/violated_sla.html'
    required_perm = 'violated sla'
    context_object_name = 'sla_violated'
    paginate_by = 7

    def get_queryset(self):
        """
        get_queryset used rather than get_context_data as it executes before the pagination takes place
        """
        queryset = self.model.objects.all()
        queryset = sorted([x for x in queryset if x.delay], key=lambda x: (-x.is_active, -x.delay))
        return queryset

