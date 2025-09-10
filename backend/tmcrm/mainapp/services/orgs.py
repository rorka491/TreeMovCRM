from django.contrib.auth import get_user_model

User = get_user_model()


def create_user_with_org(org, **kwargs):
    """
    Создаёт пользователя, закреплённого за организацией.
    """
    return User.objects.create_user(org=org, **kwargs)



