from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from srproj.accounts.models import Company, AccountProfile
from django.contrib.auth import forms as auth_forms, get_user_model

UserModel = get_user_model()


class UserRegistrationForm(auth_forms.UserCreationForm):
    CONTRACT_LENGTH = 6

    service_contract = forms.CharField(
        max_length=CONTRACT_LENGTH,
        min_length=CONTRACT_LENGTH,
        widget=forms.TextInput(attrs={'class': "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_service_contract(self):
        data = self.cleaned_data['service_contract']
        company = Company.objects.filter(contract_number__iexact=data)
        if not company:
            raise ValidationError('Invalid Service Contract')

        selected = company.first()
        if not selected.is_active:
            raise ValidationError('Company Access Restricted')

        internal = self.CONTRACT_LENGTH * '0'
        if selected.contract_number == internal:
            raise ValidationError('Registration for Customers Only')

        return data

    class Meta:
        model = UserModel
        fields = ('service_contract', 'email',)


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserPassChangeForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProfileModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = AccountProfile
        fields = ('first_name', 'last_name', 'phone')
