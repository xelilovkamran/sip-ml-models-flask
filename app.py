from flask import Flask, request, jsonify
import joblib
import logging
from api.routes.analyze import analyze

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

app.register_blueprint(analyze, url_prefix='/analyze')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
