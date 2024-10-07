import io

import numpy as np
from PIL import Image
from doc_scanner import run_scan_by_image
from flask import Blueprint, jsonify, request, send_file

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

    image = Image.open(file.stream)
    image_np = np.array(image)

    scanned_image = run_scan_by_image(image_np)

    # TODO -> convert to text

    scanned_image_pil = Image.fromarray(scanned_image)

    img_byte_arr = io.BytesIO()
    scanned_image_pil.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return send_file(img_byte_arr, mimetype='image/png')
