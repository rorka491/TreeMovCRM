import random
from django.conf import settings
from django.core.mail import send_mail


def send_email(email, code):
    subject = "Код подтверждения"
    message = f"Ваш код подтверждения: {code}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


def generate_six_digit_code() -> str:
    return str(random.randint(100000, 999999))
