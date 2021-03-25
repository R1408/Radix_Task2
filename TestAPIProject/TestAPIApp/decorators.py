from functools import wraps
import os
import jwt
from django.http import HttpResponse
from .utils import *
import json
import logging

logger = logging.getLogger(__name__)


def login_required(f):
    @wraps(f)
    def token_validator(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        logger.error('token is: {token}'.format(token=token))
        if not token:
            return HttpResponse(json.dumps(HttpErrorHandler.bad_request_error()), content_type="application/json")
        try:
            jwt.decode(token.split()[1], os.environ.get("JWT_SECRET_KEY", "xyz"), algorithms="HS256")
        except:
            logger.error('JWT Token Exception ')
            return HttpResponse(json.dumps(HttpErrorHandler.invalid_token()), content_type="application/json")
        return f(request, *args, **kwargs)

    return token_validator