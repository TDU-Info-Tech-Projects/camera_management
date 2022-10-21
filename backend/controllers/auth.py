from crypt import methods
import functools
from http.client import UNPROCESSABLE_ENTITY, UNAUTHORIZED
from select import select
from flask import jsonify, request, abort
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from os import urandom

from database.models import User
from database import engine

from controllers.main import bp
from services import valid_email
from sqlalchemy.orm import Session

MIN_PASS_LEN = 8


@bp.route("/register", methods=('GET', 'POST'))
def register():
    email = request.json["email"].strip()
    if not valid_email(email):
        abort(UNPROCESSABLE_ENTITY)

    password = request.json["password"].strip()
    if not len(password) >= MIN_PASS_LEN:
        abort(UNPROCESSABLE_ENTITY)

    first_name = request.json["first_name"].strip()
    if not len(first_name):
        abort(UNPROCESSABLE_ENTITY)

    last_name = request.json["last_name"].strip()
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


@bp.route("/login", methods=('POST',))
def login():
    email = request.json["email"].strip()
    if not valid_email(email):
        abort(UNPROCESSABLE_ENTITY)

    password = request.json["password"].strip()
    if not len(password) >= MIN_PASS_LEN:
        abort(UNPROCESSABLE_ENTITY)
        
    with Session(engine) as session:
        user = session.query(User).where(User.email_address == email).one()

        kdf = Scrypt(
            salt=bytes.fromhex(user.password_salt),
            length=256,
            n=2**14,
            r=8,
            p=1
        )

        try:
            kdf.verify(password.encode(), bytes.fromhex(user.password_hash))
        except Exception as e:
            print(e, flush=True)
            abort(UNAUTHORIZED)

        return jsonify(request.json)
