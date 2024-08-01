from flask import Blueprint, jsonify, request
import joblib
import logging
import gdown
import os
from ultralytics import YOLO
import cv2
import requests
import numpy as np


analyze = Blueprint('analyze_routes', __name__)


def download_model_from_gdrive(file_id, output_path):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)


model = YOLO('yolov8x.pt')

file_id = '1hNEbjphrlDHIKIlvRr8UD3c6lQofZpF4'
model_path = 'ml/model.pkl'  # Temporary path to store the model file

if not os.path.exists(model_path):
    download_model_from_gdrive(file_id, model_path)

try:
    with open(model_path, 'rb') as model_file:
        sentiment_model, vectorizer = joblib.load(model_file)

    if not hasattr(vectorizer, 'transform'):
        raise ValueError(
            "Loaded object 'vectorizer' is not a valid vectorizer.")

    if not hasattr(sentiment_model, 'predict'):
        raise ValueError("Loaded object 'model' is not a valid model.")
except Exception as e:
    logging.error(f"Error loading model and vectorizer: {e}")
    raise e


@analyze.route('/analyze-comment/', methods=['POST'])
def analyze_comment():
    data = request.json
    comment = data.get('comment', '')

    try:
        comment_vectorized = vectorizer.transform([comment])

        sentiment = sentiment_model.predict(comment_vectorized)[0]
        return jsonify({'sentiment': sentiment})
    except Exception as e:
        logging.error(f"Error during analysis: {e}")
        return jsonify({'error': 'Error during analysis'}), 500


@analyze.route('/analyze-comment-image/', methods=['POST'])
def analyze_comment_image():
    data = request.json
    image_url = data.get('image_url', '')
    comment = data.get('comment', '')

    if not image_url or not comment:
        return jsonify({'message': 'Şəkil linki və şərh yüklənmədi'}), 400

    try:
        # Şəkili endirib oxuyuruq
        response = requests.get(image_url)
        image = cv2.imdecode(np.frombuffer(
            response.content, np.uint8), cv2.IMREAD_COLOR)

        # Modeli istifadə edərək deteksiya
        results = model(image)

        # Debug: Detaylı məlumat ver
        logging.debug(f"Results: {results}")

        # Bıçaq deteksiyası üçün yoxlama
        knife_detected = False
        for result in results:
            for box in result.boxes:
                logging.debug(
                    f"Box Class: {box.cls}, Box Confidence: {box.conf}")
                if box.cls == 0:  # Burada 0 bıçağın sinif ID'si olaraq varsayılmışdır
                    knife_detected = True
                    break

        if knife_detected:
            sentiment = "negative"
        else:
            # Vektorlaşdırma
            comment_vectorized = vectorizer.transform([comment])

            # Sentiment analizi
            sentiment = sentiment_model.predict(comment_vectorized)[0]

        # Nəticəyə əsasən cavab
        if knife_detected:
            return jsonify({'message': 'Təhlükəli şəkil: Bıçaq aşkar edildi!', 'sentiment': sentiment}), 200
        else:
            return jsonify({'message': 'Təhlükəsiz şəkil: Bıçaq aşkar edilmədi.', 'sentiment': sentiment}), 200

    except Exception as e:
        logging.error(f"Xəta: {e}")  # Xətanın ətraflı məlumatını yazdırın
        return jsonify({'error': 'Xəta baş verdi!'}), 500
