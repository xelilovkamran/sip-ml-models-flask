from flask import Flask, request, jsonify
import logging
from api.routes.analyze import analyze

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

app.register_blueprint(analyze, url_prefix='/analyze')


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {e}")
    return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
