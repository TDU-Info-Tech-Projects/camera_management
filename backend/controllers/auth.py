import functools
from flask import jsonify

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route("/register", methods=('GET', 'POST'))
def register():
    return jsonify({"paht": "register"})