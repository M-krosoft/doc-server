import io

import numpy as np
from PIL import Image
from doc_scanner import run_scan_by_image
from flask import Blueprint, jsonify, request, send_file, render_template
from typing_extensions import deprecated

from services.vision_service import VisionService

from app import repository

doc_scanner_bp = Blueprint('doc_scanner', __name__, url_prefix='/doc-scanner')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@doc_scanner_bp.route('/scan', methods=['POST'])
def scan_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Only images are allowed."}), 400

    vision_service = VisionService()
    image_content = file.read()

    try:
        detected_text = vision_service.detect_text_in_image(image_content)
        repository.save_receipt(receipt_content=detected_text)
        return jsonify({'detected_text': detected_text})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@deprecated("This function probably will be removed in future versions")
@doc_scanner_bp.route('/scan2', methods=['POST'])
def scan_image2():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400


    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Only images are allowed."}), 400

    image = Image.open(file.stream)

    image_np = np.array(image)

    scanned_image = run_scan_by_image(image_np)


    # TODO -> convert to text then save it in db
    repository.save_receipt(receipt_content='TEST TEST')

    scanned_image_pil = Image.fromarray(scanned_image)

    img_byte_arr = io.BytesIO()
    scanned_image_pil.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return send_file(img_byte_arr, mimetype='image/png')

@doc_scanner_bp.route('/count', methods=['POST'])
def get_count():
    return repository.count_receipts(), 200


@doc_scanner_bp.route('/text-recognition', methods=['POST'])
def text_recognition():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image_content = image_file.read()

    vision_service = VisionService()

    try:
        detected_text = vision_service.detect_text_in_image(image_content)
        if detected_text:
            return jsonify({'detected_text': detected_text}), 200
        else:
            return jsonify({'error': 'No text detected'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
