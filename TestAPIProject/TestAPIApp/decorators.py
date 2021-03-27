from functools import wraps
import os
import jwt
from django.http import HttpResponse
from .utils import *
import json
import logging
from marshmallow.exceptions import ValidationError

logger = logging.getLogger(__name__)


def login_required(f):
    @wraps(f)
    def token_validator(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        logger.error(F'token is: {token}')
        if not token:
            error = HttpErrorHandler.bad_request_error()
            error['message'] = "Missing token found while processing the request"
            return HttpResponse(json.dumps(error), content_type="application/json")
        try:
            jwt.decode(token.split()[1], os.environ.get("JWT_SECRET_KEY", "xyz"), algorithms="HS256")
        except:
            logger.error('JWT Token Exception ')
            return HttpResponse(json.dumps(HttpErrorHandler.invalid_token()), content_type="application/json")
        return f(request, *args, **kwargs)

    return token_validator


def validate_api_payload(schema_class):
    def decorator(f):
        @wraps(f)
        def wrapper(request, *args, **kw):
            try:
                schema = schema_class()
                payload = schema.dump(schema.load(request.data))
                kw = {**payload, **kw}
            except ValidationError as e:
                logger.error(F'Validation Error: {e.messages}')
                error = HttpErrorHandler.bad_request_error()
                error['message'] = e.messages
                return HttpResponse(json.dumps(error), content_type="application/json")
            return f(*args, **kw)

        return wrapper

    return decorator