import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from srproj.accounts.models import Company
from srproj.tickets.models.base_models import TicketSla
from srproj.tickets.models.core_models import Ticket
from srproj.tickets.models.suppl_models import ProductFamily, Product

UserModel = get_user_model()


class TicketResolvedListViewTest(TestCase):
    product_family_data = {
        'name': 'X2020 Mobile Family',
        'domain': ProductFamily.MOBILE,
    }
    product_data = {
        'name': 'X2020_11',
        'version': 'R12',
        'stability': Product.STABLE_RELEASE,
    }
    company_customer_data = {
        'name': 'ChinaTel',
        'valid_to': datetime.datetime(2055, 1, 17),
        'contract_number': '222222',
    }
    company_internal_data = {
        'name': 'internal',
        'valid_to': datetime.datetime(2055, 1, 17),
        'contract_number': '000000',
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
        product_family = ProductFamily.objects.create(**self.product_family_data)
        self.product_data['family'] = product_family
        product = Product.objects.create(**self.product_data)
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

        ticket_data = {
            'summary': 'Something went wrong',
            'description': 'Something went wrong',
            'product': product,
            'creator': user_customer1,
            'modifier': user_customer1,
            'is_active': False,
            'state': Ticket.CLOSED,
            'assignee': user_support,
            'severity': TicketSla.objects.create(severity='Major', reaction_hours=self.reaction_hours),
            'register_date': datetime.datetime.now(),
            'resolve_due_date': datetime.datetime.now() + datetime.timedelta(hours=5),
            'resolve_date': datetime.datetime.now() + datetime.timedelta(hours=20),
        }
        self.ticket_1 = Ticket.objects.create(**ticket_data)
        self.ticket_2 = Ticket.objects.create(**ticket_data)
        self.action = 'resolved tickets'

    def test_customer_can_view_ticket_resolved_list_and_their_content_when_creator(self):
        self.client.login(**self.user_customer1_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 2)
        self.ticket_2.is_active = True
        self.ticket_2.save()
        response = self.client.get(reverse(self.action))
        self.assertEqual(len(response.context_data['object_list']), 1)

    def test_support_can_view_ticket_resolved_list_and_their_content_when_assignee(self):
        self.client.login(**self.user_support_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 2)

    def test_customer_can_view_ticket_resolved_list_but_only_their_own(self):
        self.client.login(**self.user_customer2_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 0)

    def test_care_can_view_ticket_resolved_list_of_all_customers(self):
        self.client.login(**self.user_care_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 2)

    def test_supervisor_can_view_ticket_resolved_list_of_all_customers(self):
        self.client.login(**self.user_supervisor_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets/list_tickets.html')
        self.assertEqual(len(response.context_data['object_list']), 2)

    def test_user_not_logged_in_is_redirected_at_home(self):
        response = self.client.get(reverse(self.action))
        self.assertRedirects(response, '/')
