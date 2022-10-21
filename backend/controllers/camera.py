from flask import jsonify

from flask import Blueprint

from controllers.main import bp

@bp.route("/test", methods=('GET', 'POST'))
def test():
    return jsonify({"path": "test"})

