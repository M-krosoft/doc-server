import io
import os

import numpy as np
from PIL import Image
from doc_scanner import run_scan_by_image
from flask import Flask, jsonify, request, send_file, Blueprint, render_template

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

doc_scanner_bp = Blueprint('doc_scanner', __name__)


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
    scanned_image_pil = Image.fromarray(scanned_image)

    img_byte_arr = io.BytesIO()
    scanned_image_pil.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return send_file(img_byte_arr, mimetype='image/png')


@app.route('/doc-scanner')
def index():
    return render_template('index.html')


app.register_blueprint(doc_scanner_bp, url_prefix='/doc-scanner')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
