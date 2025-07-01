import threading

_user_storage = threading.local()


def get_current_user():
    return getattr(_user_storage, "user", None)


class GetCurrentUserMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            print('Вы аунтетифицированы')
            _user_storage.user = user
        response = self.get_response(request)
        return response
