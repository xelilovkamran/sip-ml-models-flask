from flask import Blueprint, jsonify, request
import numpy as np
import joblib
import logging
import cv2
from api.helpers.helper import url_to_image


analyze = Blueprint('analyze_routes', __name__)

sentiment_model_path = 'ml/model.pkl'
image_model_path = 'ml/cascade.xml'


@analyze.route('/analyze-content', methods=['POST'])
def analyze_comment():
    try:
        with open(sentiment_model_path, 'rb') as model_file:
            sentiment_model, vectorizer = joblib.load(model_file)

        if not hasattr(vectorizer, 'transform'):
            raise ValueError(
                "Loaded object 'vectorizer' is not a valid vectorizer.")

        if not hasattr(sentiment_model, 'predict'):
            raise ValueError("Loaded object 'model' is not a valid model.")
    except Exception as e:
        return jsonify({'error': 'Error during model loading'}), 500

    data = request.json
    content = data.get('content', '')

    try:
        content_vectorized = vectorizer.transform([content])

        predicted_status = sentiment_model.predict(content_vectorized)[0]
        return jsonify({'status': predicted_status})
    except Exception as e:
        logging.error(f"Error during analysis: {e}")
        return jsonify({'error': 'Error during analysis'}), 500


@analyze.route('/analyze-image', methods=['POST'])
def analyze_comment_image():
    gun_cascade = cv2.CascadeClassifier(image_model_path)

    data = request.json
    image_url = data.get('image_url', '')
    image = url_to_image(image_url)

    if image is None:
        return jsonify({'error': 'Error during image loading'}), 500
    else:
        resized_image = cv2.resize(
            image, (500, int(image.shape[0] * 500 / image.shape[1])))

        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        gun = gun_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=20, minSize=(100, 100))

        if len(gun) > 0:
            return jsonify({'status': 'negative'})

    return jsonify({'status': 'non-negative'})
