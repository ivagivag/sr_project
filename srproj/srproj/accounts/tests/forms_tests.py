from django.test import TestCase

from srproj.accounts.forms import UserRegistrationForm
from srproj.accounts.models import Company
import datetime


class UserRegistrationFormTest(TestCase):
    company_data = {
        'name': 'ChinaTel',
        'valid_to': datetime.datetime(2055, 1, 17)
    }

    def test_user_provided_invalid_company_contract(self):
        self.company_data['contract_number'] = '888'
        self.company_data['is_active'] = True
        Company.objects.create(**self.company_data)

        form = UserRegistrationForm(data={'service_contract': '799'})
        self.assertEqual(
            form.errors['service_contract'], ['Invalid Service Contract']
        )

    def test_user_provided_company_contract_expired(self):
        self.company_data['contract_number'] = '888'
        self.company_data['is_active'] = False
        Company.objects.create(**self.company_data)

        form = UserRegistrationForm(data={'service_contract': '888'})
        self.assertEqual(
            form.errors['service_contract'], ['Company Access Restricted']
        )

    def test_user_provided_internal_company_contract_not_allowed(self):
        self.company_data['contract_number'] = '000'
        self.company_data['is_active'] = True
        Company.objects.create(**self.company_data)

        form = UserRegistrationForm(data={'service_contract': '000'})
        self.assertEqual(
            form.errors['service_contract'], ['Registration for Customers Only']
    )

    def test_user_provided_company_correct_data(self):
        self.company_data['contract_number'] = '888'
        self.company_data['is_active'] = True
        Company.objects.create(**self.company_data)
        form = UserRegistrationForm(data={'service_contract': '888'})
        self.assertNotIn('service_contract', form.errors)
