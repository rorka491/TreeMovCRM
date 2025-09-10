import threading
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from mainapp.models import User, Organization

_user_storage = threading.local()


def get_current_user() -> 'User | None':
    return getattr(_user_storage, "user", None)

def get_current_org() -> 'Organization | None':
    return getattr(_user_storage, "org", None)

class GetCurrentUserMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            _user_storage.user = user
            _user_storage.org = user.get_org()
        response = self.get_response(request)
        return response
