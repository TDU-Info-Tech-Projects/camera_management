from flask import Flask, jsonify, request
from controllers.hello import get_test_json

app = Flask(__name__)

# ルートの登録
app.route('/')(get_test_json)

app.run()
