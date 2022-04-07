from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
import datetime

from srproj.accounts.models import Company, AccountProfile

UserModel = get_user_model()


class AccountProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        company_data = {
            'name': 'ChinaTel',
            'contract_number': '888',
            'valid_to': datetime.datetime(2055, 11, 11)
        }
        company = Company.objects.create(**company_data)
        user_data = {
            'email': 'i@g.bg',
            'company': company,
        }
        UserModel.objects.create(**user_data)

    def test_first_name_has_invalid_chars_digits(self):
        account = UserModel.objects.first()
        profile_data = {
            'first_name': 'Klara123',
            'last_name': 'Simpson',
            'account': account,
        }
        profile = AccountProfile(**profile_data)
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_last_name_has_invalid_chars_digits(self):
        account = UserModel.objects.first()
        profile_data = {
            'first_name': 'Klara',
            'last_name': 'Simp&son$',
            'account': account,
        }
        profile = AccountProfile(**profile_data)
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_phone_has_invalid_chars_digits(self):
        account = UserModel.objects.first()
        profile_data = {
            'first_name': 'Klara',
            'last_name': 'Simpson',
            'phone': '%%+359 77 243',
            'account': account,
        }
        profile = AccountProfile(**profile_data)
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_all_profile_data_valid(self):
        account = UserModel.objects.first()
        profile_data = {
            'first_name': 'Klara',
            'last_name': 'Simpson',
            'phone': '+359 77 243 666',
            'account': account,
        }
        AccountProfile.objects.create(**profile_data)
        profile = AccountProfile.objects.get(account=account)
        self.assertEqual(profile_data['first_name'], profile.first_name)
        self.assertEqual(profile_data['last_name'], profile.last_name)
        self.assertEqual(profile_data['phone'], profile.phone)
