import threading
from typing import TYPE_CHECKING
from contextvars import ContextVar
from ..exceptions.user_exceptions import UserNotHasBeenGet

current_user = ContextVar("current_user", default=None)
current_org = ContextVar("current_org", default=None)

if TYPE_CHECKING:
    from mainapp.models import User, Organization

_user_storage = threading.local()


def get_current_user() -> 'User | None':
    return current_user.get()

def get_current_org() -> 'Organization | None':
    user = get_current_user() 

    if not user:
        raise UserNotHasBeenGet("Пользователь не найден")
    return user.get_org()

class GetCurrentUserMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        current_user.set(user)
        return self.get_response(request)
