from functools import wraps
from flask import request, abort, Response
from http.client import UNPROCESSABLE_ENTITY, UNAUTHORIZED
from services import valid_email
import jwt
import os

MIN_PASS_LEN = 8
JWT_SECRET = os.getenv("JWT_SECRET")


def validate_email(f):
    @wraps(f)
    def __validate_email(*args, **kwargs):
        email = request.json["email"].strip()
        if not valid_email(email):
            abort(UNPROCESSABLE_ENTITY)
        request.json["email"] = email

        return f(*args, **kwargs)
    return __validate_email


def validate_password(f):
    @wraps(f)
    def __validate_password(*args, **kwargs):
        password = request.json["password"]
        if not len(password) >= MIN_PASS_LEN:
            abort(UNPROCESSABLE_ENTITY)

        return f(*args, **kwargs)
    return __validate_password


def validate_fullname(f):
    @wraps(f)
    def __validate_fullname(*args, **kwargs):
        first_name = request.json["first_name"].strip()
        if not len(first_name):
            abort(UNPROCESSABLE_ENTITY)

        last_name = request.json["last_name"].strip()
        if not len(last_name):
            abort(UNPROCESSABLE_ENTITY)

        return f(*args, **kwargs)
    return __validate_fullname


# TODO: implement admin_only
def protected(admin_only=False):
    def _protected(f):
        @wraps(f)
        def __protected(*args, **kwargs):
            token = request.cookies.get("jwt-auth")
            try:
                userInfo = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            except:
                res = Response(status=UNAUTHORIZED)
                res.delete_cookie("jwt-auth")
                return res

            request.user = userInfo
            return f(*args, **kwargs)
        return __protected
    return _protected
