from django.contrib.auth import mixins as auth_mixin, get_user_model
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

UserModel = get_user_model()

define_perm = {
    'create tickets': ('Customer', 'Supervisor'),
    'modify tickets': ('Customer', 'Support', 'Supervisor'),
    'assign tickets': ('Supervisor',),
    'close tickets': ('Customer', 'Supervisor'),
    'delete tickets': ('Supervisor',),
    'tickets details': ('Customer', 'Support', 'Care', 'Supervisor'),
    'assess tickets': ('Customer', 'Supervisor'),
    'event log': ('Customer', 'Support', 'Care', 'Supervisor'),
    'create entry': ('Customer', 'Support', 'Supervisor'),
    'active tickets': ('Customer', 'Support', 'Care', 'Supervisor'),
    'resolved tickets': ('Customer', 'Support', 'Care', 'Supervisor'),
    'feedback': ('Care', 'Supervisor'),
    'violated sla': ('Care', 'Supervisor'),
    'create company': ('Supervisor',),
    'modify company': ('Supervisor',),
    'display company': ('Supervisor',),
    'act deact company': ('Supervisor',),
    'list companies': ('Supervisor',),
}

define_own_perm = {
    'modify tickets': ('Customer', 'Support'),
    'close tickets': ('Customer',),
    'tickets details': ('Customer', 'Support'),
    'assess tickets': ('Customer',),
    'event log': ('Customer', 'Support'),
    'create entry': ('Customer', 'Support'),
}


class HelperMixin:
    def get_ticket(self):
        tid = self.kwargs['pk'] if 'tid' not in self.kwargs else self.kwargs['tid']
        if hasattr(self, 'ticket_model'):
            ticket_model = self.ticket_model
        else:
            ticket_model = self.model
        ticket_object = ticket_model.objects.get(pk=tid)
        return ticket_object

    def user_has_perm(self):
        result = UserModel.objects.filter(pk=self.request.user.id,
                                        groups__name__in=define_perm[self.required_perm]).exists()
        return result

    def user_has_own_perm(self):
        if not self.user_has_perm():
            return False

        if self.required_perm not in define_own_perm:
            return True

        if not UserModel.objects.filter(pk=self.request.user.id,
                                        groups__name__in=define_own_perm[self.required_perm]).exists():
            return True

        ticket_object = self.get_ticket()
        if self.request.user in (ticket_object.creator, ticket_object.assignee):
            return True

        return False


class VerifyPermissionMixin(auth_mixin.UserPassesTestMixin, HelperMixin):
    def test_func(self):
        result = self.user_has_perm()
        return result


class VerifyPermissionOwnMixin(VerifyPermissionMixin):
    def test_func(self):
        result = self.user_has_own_perm()
        return result


class VerifyPermissionChangeMixin(VerifyPermissionMixin):
    def _is_ticket_active(self):
        ticket = self.get_ticket()
        return ticket.is_active

    def test_func(self):
        if not super().test_func():
            return False
        return self._is_ticket_active()


class VerifyPermissionChangeOwnMixin(VerifyPermissionChangeMixin):
    def test_func(self):
        result = super().test_func() and self.user_has_own_perm()
        return result


class VerifyPermissionRestrictMixin(VerifyPermissionMixin):
    def test_func(self):
        result = not self.request.user.is_restricted and super().test_func()
        return result


class CustomLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)
