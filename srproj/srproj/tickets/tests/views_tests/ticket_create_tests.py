import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from srproj.accounts.models import Company
from srproj.tickets.models.suppl_models import ProductFamily, Product

UserModel = get_user_model()


class CompanyCreateViewTest(TestCase):
    company_customer_data = {
        'name': 'ChinaTel',
        'valid_to': datetime.datetime(2055, 1, 17),
        'contract_number': '222',
    }
    company_internal_data = {
        'name': 'internal',
        'valid_to': datetime.datetime(2055, 1, 17),
        'contract_number': '000',
    }
    user_customer1_data = {
        'email': 'z@x.com',
        'password': '123',
    }
    user_customer2_data = {
        'email': 'c@v.com',
        'password': '123',
    }
    user_support_data = {
        'email': 'q@w.bg',
        'password': '123',
        'is_external': False,
    }
    user_supervisor_data = {
        'email': 'i@g.bg',
        'password': '123',
        'is_external': False,
    }
    user_care_data = {
        'email': 'r@t.bg',
        'password': '123',
        'is_external': False,
    }
    current_time = datetime.datetime.now()
    reaction_hours = 2

    def setUp(self):
        company_customer = Company.objects.create(**self.company_customer_data)
        company_internal = Company.objects.create(**self.company_internal_data)
        self.user_customer1_data.update({'company': company_customer})
        self.user_customer2_data.update({'company': company_customer})
        self.user_support_data.update({'company': company_internal})
        self.user_supervisor_data.update({'company': company_internal})
        self.user_care_data.update({'company': company_internal})
        user_customer1 = UserModel.objects.create_user(**self.user_customer1_data)
        user_customer2 = UserModel.objects.create_user(**self.user_customer2_data)
        user_support = UserModel.objects.create_user(**self.user_support_data)
        user_supervisor = UserModel.objects.create_user(**self.user_supervisor_data)
        user_care = UserModel.objects.create_user(**self.user_care_data)
        group_customer = Group.objects.create(name="Customer")
        group_support = Group.objects.create(name="Support")
        group_supervisor = Group.objects.create(name="Supervisor")
        group_care = Group.objects.create(name="Care")
        group_customer.user_set.add(user_customer1)
        group_customer.user_set.add(user_customer2)
        group_support.user_set.add(user_support)
        group_supervisor.user_set.add(user_supervisor)
        group_care.user_set.add(user_care)
        self.action = 'create ticket'

    def test_support_can_not_create_ticket(self):
        self.client.login(**self.user_support_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 403)

    def test_care_can_not_create_ticket(self):
        self.client.login(**self.user_care_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 403)

    def test_create_ticket_form_fields_required(self):
        self.client.login(**self.user_customer1_data)
        response = self.client.post(reverse(self.action))
        for field in ('summary', 'description', 'product', 'severity'):
            self.assertFormError(response, 'form', field, 'This field is required.')

    def test_customer_can_create_ticket(self):
        self.client.login(**self.user_customer1_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/create_ticket.html')

    def test_supervisor_can_create_ticket(self):
        self.client.login(**self.user_supervisor_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 200)

    def test_user_not_logged_in_is_redirected_at_home(self):
        response = self.client.get(reverse(self.action))
        self.assertRedirects(response, '/')