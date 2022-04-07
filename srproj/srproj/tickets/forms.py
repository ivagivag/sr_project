from django import forms
from django.contrib.auth import get_user_model

from srproj.tickets.models.core_models import Ticket, TicketWorkFlow, TicketAssessment
from srproj.tickets.models.suppl_models import Product

UserModel = get_user_model()


class TicketRegistrationForm(forms.ModelForm):
    ro_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        for field in self.ro_fields:
            if field in self.fields:
                self.fields[field].disabled = True
        self.fields['product'].queryset = Product.objects.filter(is_active=True)

    class Meta:
        model = Ticket
        fields = ('summary', 'description', 'product', 'severity',)
        widgets = {
            'summary': forms.TextInput(attrs={'placeholder': 'Summary of the issue'}),
            'description': forms.Textarea(attrs={'placeholder': '''What happened?
When did it happen?
Was it due to configuration change?'''}),
        }


class TicketModificationForm(TicketRegistrationForm):
    ro_fields = ('summary', 'description')

    state = forms.ChoiceField(choices=Ticket.RESTRICTED_CHOICES)

    class Meta:
        model = Ticket
        fields = ('summary', 'description', 'product', 'severity', 'state')


class TicketAssignForm(TicketRegistrationForm):
    ro_fields = ('summary', 'description', 'product', 'severity', 'state')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assignee'].queryset = UserModel.objects.filter(is_external=False)

    class Meta:
        model = Ticket
        fields = ('summary', 'description', 'product', 'severity', 'state', 'assignee')


class EntryRegistrationForm(forms.ModelForm):
    ro_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        for field in self.ro_fields:
            if field in self.fields:
                self.fields[field].disabled = True

    class Meta:
        model = TicketWorkFlow
        fields = ('note', 'typ')
        widgets = {
            'note': forms.Textarea(attrs={'placeholder': '''Please, write here the following notes:
------------------------------------------
Root Cause Analysis
Corrective Actions
Resolution Notes
Customer Experience
'''}),
        }


class TicketAssessmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = TicketAssessment
        exclude = ('ticket', 'creator', 'event_time')
        widgets = {
            'reaction_remark': forms.Textarea(
                attrs={'placeholder': 'Your opinion about the reaction time of our support team',
                       'rows': 4}),
            'resolve_remark': forms.Textarea(
                attrs={'placeholder': 'Your opinion about the resolution provided by our support team',
                       'rows': 4}),
            'overall_remark': forms.Textarea(
                attrs={'placeholder': 'Your overall satisfaction of service we provide',
                       'rows': 4}),
        }
