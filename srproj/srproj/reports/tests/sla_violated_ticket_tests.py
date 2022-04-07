import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from srproj.accounts.models import Company
from srproj.tickets.models.base_models import TicketSla
from srproj.tickets.models.core_models import Ticket
from srproj.tickets.models.suppl_models import ProductFamily, Product
from copy import deepcopy

UserModel = get_user_model()


class TicketSlaViolatedViewTest(TestCase):
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
    customer_group = Group.objects.get(name='Customer')

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
            'assignee': user_support,
            'severity': TicketSla.objects.create(severity='Major', reaction_hours=self.reaction_hours),
            'register_date': self.current_time,
        }
        ticket_act_delayed_data = deepcopy(ticket_data)
        ticket_act_delayed_data.update({
            'is_active': True,
            'resolve_due_date': self.current_time - datetime.timedelta(hours=1),
        })
        ticket_act_data = deepcopy(ticket_data)
        ticket_act_data.update({
            'is_active': True,
            'resolve_due_date': self.current_time + datetime.timedelta(hours=1),
        })
        ticket_inact_delayed_data = deepcopy(ticket_data)
        ticket_inact_delayed_data.update({
            'is_active': False,
            'resolve_due_date': self.current_time + datetime.timedelta(hours=1),
            'resolve_date': self.current_time + datetime.timedelta(hours=2),
        })
        ticket_inact_data = deepcopy(ticket_data)
        ticket_inact_data.update({
            'is_active': False,
            'resolve_due_date': self.current_time + datetime.timedelta(hours=2),
            'resolve_date': self.current_time + datetime.timedelta(hours=1),
        })
        self.ticket_act_ok = Ticket.objects.create(**ticket_act_data)
        self.ticket_act_delayed = Ticket.objects.create(**ticket_act_delayed_data)
        self.ticket_inact_ok = Ticket.objects.create(**ticket_inact_data)
        self.ticket_inact_delayed = Ticket.objects.create(**ticket_inact_delayed_data)
        self.action = 'violated sla'

    def test_customer_creator_cannot_view_sla_violated_tickets_at_all(self):
        self.client.login(**self.user_customer1_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 403)

    def test_customer_creator_non_cannot_view_sla_violated_tickets_at_all(self):
        self.client.login(**self.user_customer2_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 403)

    def test_care_can_view_all_sla_violated_tickets_of_all_customers(self):
        self.client.login(**self.user_care_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['object_list']), 2)

    def test_supervisor_can_view_all_sla_violated_tickets_of_all_customers(self):
        self.client.login(**self.user_supervisor_data)
        response = self.client.get(reverse(self.action))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/violated_sla.html')
        self.assertEqual(len(response.context_data['object_list']), 2)

    def test_user_not_logged_in_is_redirected_at_home(self):
        response = self.client.get(reverse(self.action))
        self.assertRedirects(response, '/')
