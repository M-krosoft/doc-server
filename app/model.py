from app.app import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2048), nullable=False)
    price = db.Column(db.Float, nullable=False)

    receipt_id = db.Column(db.Integer, db.ForeignKey('receipt_data.id'), nullable=False)
    receipt = db.relationship('ReceiptData', back_populates='products')


class ReceiptData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(2048), nullable=False)

    products = db.relationship('Product', back_populates='receipt', lazy=True)
