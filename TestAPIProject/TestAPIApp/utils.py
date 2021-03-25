import base64

from marshmallow import fields


def encode_string(string):
    sample_string_bytes = string.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string


def decode_string(string):
    base64_bytes = string.encode("ascii")
    sample_string_bytes = base64.b64decode(base64_bytes)
    decode_str = sample_string_bytes.decode("ascii")
    return decode_str


class HttpErrorHandler:
    @staticmethod
    def make_error_response(http_status=500, error_code='', error_message='', ok=False):
        return {
            'ok': ok,
            'error': error_code,
            'message': error_message,
            "status_code": http_status
        }

    @staticmethod
    def invalid_token():
        return HttpErrorHandler.make_error_response(400, "INVALID_TOKEN", "Invalid Token Error")

    @staticmethod
    def resource_not_found_error():
        return HttpErrorHandler.make_error_response(404, "NOT_FOUND_ERROR", "User id is not found")

    @staticmethod
    def application_error():
        return HttpErrorHandler.make_error_response(500, "SERVER_ERROR",
                                                    "Something went wrong while processing this request")

    @staticmethod
    def invalid_authentication():
        return HttpErrorHandler.make_error_response(401, "INVALID_AUTHENTICATION", "Oops! Couldn't find your account.")

    @staticmethod
    def bad_request_error():
        return HttpErrorHandler.make_error_response(400, "BAD_REQUEST",
                                                    "Missing token found while processing the request.")

    @staticmethod
    def insufficient_permission_error():
        return HttpErrorHandler.make_error_response(403, "INSUFFICIENT_PERMISSION",
                                                    "Insufficient permission on this Account")

    @staticmethod
    def invalid_email():
        return HttpErrorHandler.make_error_response(400, "INVALID_EMAIL",
                                                    "Please Enter valid Email")

    @staticmethod
    def invalid_password():
        return HttpErrorHandler.make_error_response(400, "INVALID_PASSWORD",
                                                    "Password should be minimum 8 character")

    @staticmethod
    def user_already_exist():
        return HttpErrorHandler.make_error_response(409, "USER_ALREADY_EXIST",
                                                    "User already exists. Please sign in with your credentials")


user_details_response = {
    "ok": True,
    "details": fields.Raw(default={})
}

user_list_response = {
    "ok": True,
    "user_list": fields.Raw(default={})
}

user_account_created = {
    "ok": True,
    "message": "Successfully account created",
    "user_id": fields.Integer
}

user_account_updated = {
    "ok": True,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String
}
