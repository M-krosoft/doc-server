from app.app import db


class ReceiptData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2048), nullable=False)
