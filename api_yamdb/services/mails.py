from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from services.users import get_user_object

from api_yamdb.settings import DEFAULT_FROM_EMAIL


def create_confirmation_code_and_send_email(username: str, email: str) -> None:
    """Создает код верификации и отправляет на электронную почту."""

    user = get_user_object(username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Confirmation code',
        message=f'Your confirmation code: {confirmation_code}',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[email, ])
