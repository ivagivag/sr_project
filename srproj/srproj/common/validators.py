import re

from django.core.exceptions import ValidationError


def validate_name(value):
    """
    Validate the user's names so that only letters, dash and apostrophe are allowed
    """
    if not re.match(pattern=r"^[-a-zA-Zа-яА-Я']+$", string=value):
        raise ValidationError("Ensure this value contains only symbols suitable for name.")
    return None


def validate_phone(value):
    """
    Validate the user's phone number so that only digits, space and plus sign are allowed
    """
    if not re.match(pattern=r"^[+0-9 ']+$", string=value):
        raise ValidationError("Ensure the phone contains only digits, plus and space.")
    return None
