from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.authenticator = JWTAuthentication()

    def __call__(self, request):
        try:
            user_auth_tuple = self.authenticator.authenticate(request)
            if user_auth_tuple is not None:
                request.user, _ = user_auth_tuple
        except Exception:
            pass

        return self.get_response(request)
