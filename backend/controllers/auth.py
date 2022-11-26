from datetime import datetime, timedelta
from http.client import OK, UNPROCESSABLE_ENTITY, UNAUTHORIZED
from flask import jsonify, request, abort, Response
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from os import urandom
from database.models import User
from database import engine
from controllers.main import bp
from services import validate_email, validate_password
from sqlalchemy.orm import Session
from services.middleware import validate_fullname, protected
import jwt
import os

JWT_SECRET = os.getenv("JWT_SECRET")


@bp.route("/register", methods=('POST',))
@validate_email
@validate_password
@validate_fullname
def register():
    email = request.json["email"]
    password = request.json["password"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]

    if not len(last_name):
        abort(UNPROCESSABLE_ENTITY)

    salt = urandom(16)
    kdf = Scrypt(
        salt=salt,
        length=256,
        n=2**14,
        r=8,
        p=1
    )

    hashed = kdf.derive(password.encode())

    user = User(
        email_address=email,
        password_hash=hashed.hex(),
        password_salt=salt.hex(),
        first_name=first_name,
        last_name=last_name,
    )

    with Session(engine) as session, session.begin():
        session.add(user)

    return jsonify(request.json)


@bp.route("/unregister", methods=('POST',))
@protected(admin_only=True)
def unregister():
    req = request.json
    with Session(engine) as session, session.begin():
        user = session.query(User).where(User.email_address == req["email"]).one()
        session.delete(user)
        session.commit()
    return Response(status=OK)


ADMIN_EMAIL = os.environ.get("ADMIN")

@bp.route("/login", methods=('POST',))
@validate_email
@validate_password
def login():
    email = request.json["email"]
    password = request.json["password"]

    with Session(engine) as session:
        user = session.query(User).where(
            User.email_address == email
        ).one()

        kdf = Scrypt(
            salt=bytes.fromhex(user.password_salt),
            length=256,
            n=2**14,
            r=8,
            p=1
        )

        try:
            kdf.verify(
                password.encode(),
                bytes.fromhex(user.password_hash)
            )
        except Exception as e:
            abort(UNAUTHORIZED)

        exp = datetime.now() + timedelta(hours=24)
        token = jwt.encode(
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email_address": user.email_address,
                "exp":  exp,
                "is_admin": user.email_address == ADMIN_EMAIL
            },
            JWT_SECRET,
            algorithm="HS256"
        )

        res = Response(status=OK)
        # TODO: same origin policy for csrf protection
        res.set_cookie(key="jwt-auth", value=token, max_age=86400)
        return res


@bp.route("/logout", methods=('POST',))
def logout():
    res = Response(status=OK)
    res.delete_cookie("jwt-auth")
    return res


@bp.route("/authenticate")
@protected()
def authenticate():
    return jsonify(request.user)
