from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from srproj.accounts.models import AccountProfile, Company
from srproj.accounts.forms import UserRegistrationForm, ProfileModelForm, UserLoginForm, \
    UserPassChangeForm

UserModel = get_user_model()


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            company_cn = form.cleaned_data['service_contract']
            company = Company.objects.get(contract_number__iexact=company_cn)
            user.company = company
            user.save()
            profile = AccountProfile(
                account=user,
            )
            profile.save()
            customer = Group.objects.get(name='Customer')
            customer.user_set.add(user)
            login(request, user)
            return redirect('user profile', pk=user.pk)
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def user_profile(request, pk):
    if request.user.is_anonymous:
        return redirect('main page')

    profile = AccountProfile.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProfileModelForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main page')
    else:
        form = ProfileModelForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('main page')


def logout_view(request):
    logout(request)
    return redirect('main page')


class UserPassChangeView(auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = UserPassChangeForm
    success_url = reverse_lazy('main page')
