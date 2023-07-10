from rest_framework.exceptions import APIException

class ModelInstanceExist(APIException):
    status_code = 400
    default_detail = "model instance exist"
    default_code = "instance_exist"