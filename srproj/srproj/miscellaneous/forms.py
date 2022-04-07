from django import forms

from srproj.accounts.models import Company
from srproj.tickets.models.suppl_models import Product, ProductFamily


class ProductFamilyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ProductFamily
        fields = '__all__'


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Company
        exclude = ('update_time', 'is_active')


class CompanyActDeactForm(CompanyForm):
    ro_fields = ('name', 'contract_number', 'valid_to')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.ro_fields:
            if field in self.fields:
                self.fields[field].disabled = True

    class Meta:
        model = Company
        fields = ('name', 'contract_number', 'valid_to')
