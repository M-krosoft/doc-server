from flask import Flask, Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy

from app.app_config import Config

app_bp = Blueprint('app_bp', __name__)
db = SQLAlchemy()


@app_bp.route('/doc-scanner')
def index():
    return render_template('index.html')


def create_app(config: Config):
    from app.controller import doc_scanner_bp

    _app = Flask(__name__)
    _app.config.from_object(config)

    _app.register_blueprint(app_bp)
    _app.register_blueprint(doc_scanner_bp)

    db.init_app(_app)
    with _app.app_context():
        db.create_all()

    return _app
