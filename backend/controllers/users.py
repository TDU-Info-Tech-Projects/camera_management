from flask import jsonify

from controllers.main import bp
from http.client import OK
from flask import jsonify, request, Response
from database import engine
from controllers.main import bp
from database.models import User
from sqlalchemy.orm import Session
from sqlalchemy import select
from services.middleware import protected


@bp.route("/test", methods=('GET', 'POST'))
def test():
    return jsonify({"path": "test"})

@bp.route("/admin/users")
@protected(admin_only=True)
def get_users():
    with Session(engine) as session:
        result = session.query(User).all()
        return jsonify(result)

def edit_user():
    pass


def delete_user():
    pass
