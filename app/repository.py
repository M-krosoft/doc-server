from app import db
from app.model import ReceiptData


def save_receipt(receipt_content: str):
    receipt_data = ReceiptData()
    receipt_data.content = receipt_content
    db.session.add(receipt_data)
    db.session.commit()


def count_receipts():
    return ReceiptData.query.all().count()
