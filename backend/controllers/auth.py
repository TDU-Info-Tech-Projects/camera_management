import functools
from http.client import UNPROCESSABLE_ENTITY
from flask import jsonify, request, abort
import bcrypt

from database.models import User

from controllers.main import bp
from services import valid_email

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

     


    return jsonify(request.json)