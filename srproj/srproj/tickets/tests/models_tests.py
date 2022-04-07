import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from srproj.accounts.models import Company
from srproj.tickets.models.base_models import TicketSla
from srproj.tickets.models.core_models import Ticket, TicketAssessment
from srproj.tickets.models.suppl_models import ProductFamily, Product

UserModel = get_user_model()


class TicketModelTest(TestCase):
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
        'is_active': True,
    }
    company_data = {
        'name': 'ChinaTel',
        'valid_to': datetime.datetime(2055, 1, 17)
    }
    user_data = {
        'email': 'i@g.bg',
    }

    def setUp(self):
        product_family = ProductFamily.objects.create(**self.product_family_data)
        self.product_data['family'] = product_family
        product = Product.objects.create(**self.product_data)
        company = Company.objects.create(**self.company_data)
        self.user_data.update({'company': company})
        user = UserModel.objects.create(**self.user_data)
        current_time = datetime.datetime.now()
        reaction_hours = 2
        ticket_data = {
            'summary': 'Something went wrong',
            'description': 'Something went wrong',
            'product': product,
            'creator': user,
            'modifier': user,
            'severity': TicketSla.objects.create(severity='Major',reaction_hours=reaction_hours),
            'state': Ticket.OPEN,
            'register_date': datetime.datetime.now(),
            'resolve_due_date': current_time + datetime.timedelta(hours=reaction_hours)
        }
        self.ticket = Ticket.objects.create(**ticket_data)

    def test_if_ticket_property_is_delayed_is_set_correctly_true_when_active(self):
        self.ticket.resolve_due_date = datetime.datetime.now() - datetime.timedelta(seconds=65)
        self.assertTrue(self.ticket.is_delayed)

    def test_if_ticket_property_is_delayed_is_set_correctly_false_when_active(self):
        self.ticket.resolve_due_date = datetime.datetime.now() + datetime.timedelta(seconds=65)
        self.assertFalse(self.ticket.is_delayed)

    def test_if_ticket_property_is_delayed_is_set_correctly_true_when_not_active(self):
        self.ticket.is_active = False
        self.ticket.resolve_date = self.ticket.resolve_due_date + datetime.timedelta(seconds=65)
        self.assertTrue(self.ticket.is_delayed)

    def test_if_ticket_property_is_delayed_is_set_correctly_false_when_not_active(self):
        self.ticket.is_active = False
        self.ticket.resolve_date = self.ticket.resolve_due_date - datetime.timedelta(seconds=65)
        self.assertFalse(self.ticket.is_delayed)


class TicketAssessmentTest(TestCase):
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
        'is_active': True,
    }
    company_data = {
        'name': 'ChinaTel',
        'valid_to': datetime.datetime(2055, 1, 17)
    }
    user_data = {
        'email': 'i@g.bg',
    }

    def setUp(self):
        product_family = ProductFamily.objects.create(**self.product_family_data)
        self.product_data['family'] = product_family
        product = Product.objects.create(**self.product_data)
        company = Company.objects.create(**self.company_data)
        self.user_data.update({'company': company})
        user = UserModel.objects.create(**self.user_data)
        current_time = datetime.datetime.now()
        reaction_hours = 2
        ticket_data = {
            'summary': 'Something went wrong',
            'description': 'Something went wrong',
            'product': product,
            'creator': user,
            'modifier': user,
            'severity': TicketSla.objects.create(severity='Major',reaction_hours=reaction_hours),
            'state': Ticket.OPEN,
            'register_date': datetime.datetime.now(),
            'resolve_due_date': current_time + datetime.timedelta(hours=reaction_hours)
        }
        ticket = Ticket.objects.create(**ticket_data)
        self.ticket_assess_data = {
            'ticket': ticket,
            'creator': user,
        }

    def test_is_negative_property_correct_when_at_least_one_negative_choice(self):
        self.ticket_assess_data.update({
            'reaction': TicketAssessment.POOR,
            'resolve': TicketAssessment.GOOD,
            'overall': TicketAssessment.EXCELLENT,
        })
        ticket_assess = TicketAssessment(**self.ticket_assess_data)
        self.assertTrue(ticket_assess.is_negative)

    def test_is_negative_property_correct_when_all_choices_positive(self):
        self.ticket_assess_data.update({
            'reaction': TicketAssessment.VERY_GOOD,
            'resolve': TicketAssessment.GOOD,
            'overall': TicketAssessment.EXCELLENT,
        })
        ticket_assess = TicketAssessment(**self.ticket_assess_data)
        self.assertFalse(ticket_assess.is_negative)