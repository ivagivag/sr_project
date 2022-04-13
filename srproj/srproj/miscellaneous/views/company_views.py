from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from srproj.accounts.models import Company
from srproj.common.view_mixins import VerifyPermissionMixin, CustomLoginRequiredMixin
from django.views import generic as views

from srproj.miscellaneous.forms import CompanyForm, CompanyActDeactForm, ProductFamilyForm, ProductForm

UserModel = get_user_model()


class CompanyCreateView(CustomLoginRequiredMixin, VerifyPermissionMixin, views.CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'misc/create_company_contract.html'
    success_url = reverse_lazy('list companies')
    required_perm = 'create company'


class CompanyModifyView(CustomLoginRequiredMixin, VerifyPermissionMixin, views.UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'misc/modify_company_contract.html'
    required_perm = 'modify company'

    def get_success_url(self):
        return reverse_lazy('display company', kwargs={'pk': self.object.pk})


class CompanyDisplayView(CustomLoginRequiredMixin, VerifyPermissionMixin, views.DetailView):
    model = Company
    template_name = 'misc/display_company_contract.html'
    required_perm = 'display company'

    def get_success_url(self):
        return reverse_lazy('list companies', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer_accounts = UserModel.objects.filter(company_id=self.kwargs['pk'])
        customer_active = []
        customer_blocked = []
        customer_restricted = []

        for user in customer_accounts:
            if user.is_active:
                customer_active.append(user)
            else:
                customer_blocked.append(user)
            if user.is_restricted:
                customer_restricted.append(user)

        context.update({
            'customer_active': customer_active,
            'customer_blocked': customer_blocked,
            'customer_restricted': customer_restricted,
        })
        return context


class CompanyListView(CustomLoginRequiredMixin, VerifyPermissionMixin, views.ListView):
    model = Company
    template_name = 'misc/list_companies.html'
    required_perm = 'list companies'

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.exclude(name__iexact='internal')
        return query_set


class CompanyActDeactView(CustomLoginRequiredMixin, VerifyPermissionMixin, views.UpdateView):
    model = Company
    form_class = CompanyActDeactForm
    template_name = 'misc/act_deact_company_contract.html'
    required_perm = 'act deact company'

    def form_valid(self, form):
        action = self.kwargs['action']
        action = action.lower()
        company_id = form.instance.pk
        restricted = None
        customer_accounts = UserModel.objects.filter(company_id=company_id)

        if action == 'activate':
            form.instance.is_active = True
            form.save()
            restricted = False
        elif action == 'deactivate':
            form.instance.is_active = False
            form.save()
            restricted = True

        if customer_accounts:
            for u in customer_accounts:
                u.is_restricted = restricted
                u.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('display company', kwargs={
            'pk': self.object.pk,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        action = self.kwargs['action']
        context['action'] = action.capitalize()

        return context
