from flask import Flask, Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy

from app.app_config import _Config

app_bp = Blueprint('app_bp', __name__)
db = SQLAlchemy()


@app_bp.route('/doc-scanner')
def index():
    return render_template('index.html')


def create_app(config: _Config):
    from app.controller import DocScanController

    _app = Flask(__name__)
    _app.config.from_object(config)

    doc_scan_controller = DocScanController(config.GOOGLE_API_KEY)
    doc_scanner_bp = doc_scan_controller.create_blueprint()

    _app.register_blueprint(app_bp)
    _app.register_blueprint(doc_scanner_bp)

    db.init_app(_app)
    with _app.app_context():
        db.create_all()

    return _app
