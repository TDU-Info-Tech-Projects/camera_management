from flask import jsonify

incomes = [
    {'api': 'camera rental', 'message': 'test000'}
]


def get_test_json():
    return jsonify(incomes)
