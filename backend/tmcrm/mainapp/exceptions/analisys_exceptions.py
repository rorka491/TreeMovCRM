from rest_framework.exceptions import APIException



class HasNoStudentsSnapShot(APIException):
    status_code = 404
    default_detail = "Can not found snapshot"


class HasNoGradesForPeriod(APIException):
    status_code = 404
    default_detail = "Can not found grades rate for current period"


class HasNoAttendanceForPeriod(APIException):
    ...
