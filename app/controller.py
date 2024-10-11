from flask import Blueprint, jsonify, request, send_file

from app.exceptions import InvalidFileExtensionError, RecognizeTextNotImplementedError
from app.services.doc_scanner_port import DocScanPort, DocScanApiKeyAdapter, DocScanNoApiKeyAdapter


class DocScanController:
    def __init__(self, google_api_key: str = ''):
        self.google_api_key = google_api_key
        self.doc_scan_port = self._prepare_doc_scanner_port()

    def _prepare_doc_scanner_port(self) -> DocScanPort:
        if self.google_api_key is not None and len(self.google_api_key) > 0:
            return DocScanApiKeyAdapter(self.google_api_key)
        else:
            return DocScanNoApiKeyAdapter()

    def _scan_image(self):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        try:
            scanned_image_bytes = self.doc_scan_port.scan_image(file)
            return send_file(scanned_image_bytes, mimetype='image/png')
        except InvalidFileExtensionError:
            return jsonify({"error": "File type not allowed. Only images are allowed."}), 400

    def _recognize_text(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file = request.files['file']
        try:
            recognized_text = self.doc_scan_port.recognize_text(file)
            if recognized_text:
                return jsonify({'detected_text': recognized_text}), 200
            else:
                return jsonify({'error': 'No text recognized'}), 204

        except RecognizeTextNotImplementedError:
            return jsonify({'error': 'Currently text recognition is turned off.'}), 404

    def _count_receipts(self):
        return self.doc_scan_port.count_receipts()

    def create_blueprint(self) -> Blueprint:
        doc_scanner_bp = Blueprint('doc_scanner', __name__, url_prefix='/doc-scanner')

        @doc_scanner_bp.route('/scan', methods=['POST'])
        def scan_image():
            return self._scan_image()

        @doc_scanner_bp.route('/recognize', methods=['POST'])
        def recognize_text():
            return self._recognize_text()

        @doc_scanner_bp.route('/count', methods=['GET'])
        def count_receipts():
            count = self._count_receipts()
            return jsonify({'count': count}), 200

        return doc_scanner_bp
