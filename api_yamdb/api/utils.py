from string import ascii_uppercase, digits
from random import choices

from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


CODE_LENGTH = 8


def send_confirmation_mail(email, code):
    """Send confirmation mail to mentionde mail with confirmation code."""
    send_mail(
        'Confirmation code',
        'Application for registration on the yam_db service '
        'has been received from your email address. If it is not you, '
        f'ignore the message. There is your conformation code: {code}',
        'confirmation@yamdb.com',
        [email],
        fail_silently=False,
    )


def get_confirmation_code():
    """Generate confirmation code"""
    return ''.join(choices(ascii_uppercase + digits, k=CODE_LENGTH))


def get_tokens_for_user(user):
    """Get token for user"""
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }
