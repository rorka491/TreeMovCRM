import random
from typing import TYPE_CHECKING
from django.conf import settings      
from django.core.mail import send_mail

if TYPE_CHECKING:
    from .models import Invite

def send_email(email: str, code: str) -> bool:
    """
    Отправляет код подтверждения на email
    Возвращает True если отправка успешна, False если нет
    """
    try:
        subject = "Код подтверждения регистрации"
        message = f"""
Здравствуйте!

Ваш код подтверждения для регистрации в системе: {code}

Код действителен в течение 5 минут.

Если вы не запрашивали этот код, проигнорируйте это письмо.
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        print(f"Код {code} отправлен на email: {email}")
        return True
    except Exception as e:
        print(f"Ошибка отправки email на {email}: {e}")
        return False


def generate_six_digit_code() -> str:
    return str(random.randint(100000, 999999))