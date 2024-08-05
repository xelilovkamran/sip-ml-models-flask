from flask import Flask, jsonify
import logging
from api.routes.analyze import analyze
from api.helpers.helper import download_model_from_gdrive
import os

sentiment_model_path = 'ml/model.pkl'
image_model_path = 'ml/cascade.xml'

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

if not os.path.exists(sentiment_model_path):
    download_model_from_gdrive(
        '1z2fnCNCd2ZDzwE0QS8qRy6k-lfa0f9mz', sentiment_model_path)

if not os.path.exists(image_model_path):
    download_model_from_gdrive(
        '1rBZTHd4TT09hRtfkfZ-yFcm1VJ3GyK8F', image_model_path)

app.register_blueprint(analyze, url_prefix='/analyze')


@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"An error occurred: {e}")
    return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
