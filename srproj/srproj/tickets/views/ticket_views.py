from datetime import datetime, timedelta

from django.contrib.auth.models import Group
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import get_user_model
from srproj.tickets.forms import TicketRegistrationForm, TicketModificationForm, TicketAssignForm
from srproj.tickets.models.core_models import Ticket, TicketWorkFlow, TicketAssessment
from srproj.common.view_mixins import VerifyPermissionMixin, \
    VerifyPermissionOwnMixin, VerifyPermissionRestrictMixin, CustomLoginRequiredMixin, VerifyPermissionChangeOwnMixin, \
    VerifyPermissionChangeMixin

UserModel = get_user_model()


def display_main_page(request):
    """
    Different main pages are displayed based on the fact whether the user has been authenticated or not
    """
    if request.user.is_authenticated:
        return render(request, 'base/index_private.html')
    else:
        return render(request, 'base/index_public.html')


class TicketCreateView(CustomLoginRequiredMixin, VerifyPermissionRestrictMixin, views.CreateView):
    form_class = TicketRegistrationForm
    template_name = 'tickets/create_ticket.html'
    success_url = reverse_lazy('active tickets')
    required_perm = 'create tickets'

    def form_valid(self, form):
        """
        Set the fields, which are mandatory but intended to be automatically populated
        """
        form.instance.creator = self.request.user
        form.instance.modifier = self.request.user
        form.instance.state = form.instance.OPEN
        sla_hours = form.instance.severity.reaction_hours
        form.instance.register_date = datetime.now()
        form.instance.resolve_due_date = form.instance.register_date + timedelta(hours=sla_hours)

        return super().form_valid(form)


class TicketModifyView(CustomLoginRequiredMixin, VerifyPermissionChangeOwnMixin, views.UpdateView):
    form_class = TicketModificationForm
    template_name = 'tickets/modify_ticket.html'
    model = Ticket
    required_perm = 'modify tickets'

    def form_valid(self, form):
        """
        Save the form only if the tickets is active, otherwise - ignore it and redirect to the success_url
        Set the fields, which are mandatory but intended to be automatically populated
        If an attempt is made to save the same form (changed_data is empty)
        do not save the form and only redirect to the success_url
        This has to do with the Event Log and prevents dummy records
        """
        if not form.instance.is_active or not form.changed_data:
            return HttpResponseRedirect(self.get_success_url())

        sla_hours = form.instance.severity.reaction_hours
        form.instance.resolve_due_date = form.instance.register_date + timedelta(hours=sla_hours)
        form.instance.modifier = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ticket details', kwargs={'pk': self.object.pk})


class TicketAssignView(CustomLoginRequiredMixin, VerifyPermissionChangeMixin, views.UpdateView):
    form_class = TicketAssignForm
    template_name = 'tickets/assign_ticket.html'
    success_url = reverse_lazy('main page')
    model = Ticket
    required_perm = 'assign tickets'

    def form_valid(self, form):
        """
        Save the form only if the ticket is active, otherwise - ignore it and redirect to the success_url
        Set the fields, which are mandatory but intended to be automatically populated
        If an attempt is made to save the same form (changed_data is empty)
        do not save the form and only redirect to the success_url
        This has to do with the Event Log and prevents dummy records
        """
        if not form.instance.is_active or not form.changed_data:
            return HttpResponseRedirect(self.get_success_url())

        form.instance.state = form.instance.ASSIGNED
        form.instance.modifier = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ticket details', kwargs={'pk': self.object.pk})


class TicketCloseView(CustomLoginRequiredMixin, VerifyPermissionChangeOwnMixin, views.UpdateView):
    template_name = 'tickets/close_ticket.html'
    model = Ticket
    fields = ()
    required_perm = 'close tickets'

    def form_valid(self, form):
        """
        Save the form only if the ticket is active, otherwise - ignore it and redirect to the success_url
        This has to do with the Event Log and prevents dummy records
        """
        if not form.instance.is_active:
            return HttpResponseRedirect(self.get_success_url())

        form.instance.state = form.instance.CLOSED
        form.instance.modifier = self.request.user
        form.instance.resolve_date = datetime.now()
        form.instance.is_active = False

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('assess ticket', kwargs={'tid': self.object.pk})


class TicketDeleteView(CustomLoginRequiredMixin, VerifyPermissionChangeOwnMixin, views.DeleteView):
    template_name = 'tickets/delete_ticket.html'
    success_url = reverse_lazy('main page')
    model = Ticket
    required_perm = 'delete tickets'


class TicketDisplayView(CustomLoginRequiredMixin, VerifyPermissionOwnMixin, views.DetailView):
    model = Ticket
    template_name = 'tickets/display_ticket.html'
    required_perm = 'tickets details'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.object
        entries = TicketWorkFlow.objects.filter(ticket=ticket).order_by('-event_time')
        assessment = TicketAssessment.objects.filter(ticket=ticket)
        context.update(
            {
                'item': ticket,
                'entries': entries,
                'assessments': assessment,
            }
        )
        return context


class TicketListView(CustomLoginRequiredMixin, VerifyPermissionMixin, views.ListView):
    model = Ticket
    template_name = 'tickets/list_tickets.html'
    context_object_name = 'tickets'
    paginate_by = 3
    required_perm = None
    category = None
    active = None

    def get_queryset(self):
        """
        Filter out the queryset, so that only the customer own records as well as the support assignee ones
        are presented.
        Show the newest records first.
        """
        query_set = super().get_queryset().select_related()
        user_groups = self.request.user.groups.all()
        if Group.objects.get(name='Customer') in user_groups:
            return query_set.filter(Q(creator=self.request.user) & Q(is_active=self.active)).order_by('-register_date')
        elif Group.objects.get(name='Support') in user_groups:
            return query_set.filter(Q(assignee=self.request.user) & Q(is_active=self.active)).order_by('-register_date')

        return query_set.filter(is_active=self.active).order_by('-register_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category

        return context


class TicketActiveView(TicketListView):
    required_perm = 'active tickets'
    category = 'Active'
    active = True


class TicketResolvedView(TicketListView):
    required_perm = 'resolved tickets'
    category = 'Resolved'
    active = False


def resource_not_found(request, exception, template_name='base/404.html'):
    """
    Custom 404 NotFound page
    The status code must be passed on to render, otherwise status code 200 is returned,
    which compromises the Unit tests
    """
    return render(request, template_name, status=404)


def forbidden(request, exception, template_name='base/403.html', status_code=403):
    """
    Custom 403 Forbidden page
    The status code must be passed on to render, otherwise status code 200 is returned,
    which compromises the Unit tests
    """
    return render(request, template_name, status=403)
