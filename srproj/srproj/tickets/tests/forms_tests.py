import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from srproj.accounts.models import Company
from srproj.tickets.forms import TicketRegistrationForm, TicketAssignForm
from srproj.tickets.models.suppl_models import Product, ProductFamily

UserModel = get_user_model()


class TicketRegistrationFormTest(TestCase):
    product_family_data = {
        'name': 'X2020 Mobile Family',
        'domain': ProductFamily.MOBILE,
    }
    product_data = {
        'name': 'X2020_11',
        'version': 'R12',
        'stability': Product.STABLE_RELEASE,
    }
    ticket_data = {
        'summary': 'Mobile station issue',
        'description': 'Mobile station issue',

    }

    def test_product_queryset_contains_no_data_when_there_are_no_active_products(self):
        product_family = ProductFamily.objects.create(**self.product_family_data)
        self.product_data['family'] = product_family
        self.product_data['is_active'] = False
        product = Product.objects.create(**self.product_data)
        form = TicketRegistrationForm()
        self.assertEqual(len(form.fields['product'].queryset), 0)

    def test_product_queryset_contains_data_when_there_are_active_products(self):
        product_family = ProductFamily.objects.create(**self.product_family_data)
        self.product_data['family'] = product_family
        self.product_data['is_active'] = True
        product = Product.objects.create(**self.product_data)
        form = TicketRegistrationForm()
        self.assertEqual(len(form.fields['product'].queryset), 1)


class TicketAssignFormTest(TestCase):
    company_data = {
        'name': 'ChinaTel',
        'valid_to': datetime.datetime(2055, 1, 17)
    }
    user_data = {
        'email': 'i@g.bg',
    }

    def test_assignee_queryset_contains_no_data_when_there_is_no_staff(self):
        company = Company.objects.create(**self.company_data)
        self.user_data.update({
            'is_external': True,
            'company': company,
        })
        UserModel.objects.create(**self.user_data)
        form = TicketAssignForm()
        self.assertEqual(len(form.fields['assignee'].queryset), 0)

    def test_assignee_queryset_contains_data_when_there_is_staff(self):
        company = Company.objects.create(**self.company_data)
        self.user_data.update({
            'is_external': False,
            'company': company,
        })
        UserModel.objects.create(**self.user_data)
        form = TicketAssignForm()
        self.assertEqual(len(form.fields['assignee'].queryset), 1)
