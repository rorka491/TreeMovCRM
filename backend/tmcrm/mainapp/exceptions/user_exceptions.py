from rest_framework.exceptions import APIException

class UserNotHasBeenGet(APIException):
    status_code = 400
    default_detail = "Пользователь не был получен ни одним доступным образом"
    default_code = "user_not_found"


