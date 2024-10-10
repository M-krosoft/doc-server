from app import db
from app.model import ReceiptData, Product


def save_receipt(receipt_content: str):
    receipt_data = ReceiptData()
    receipt_data.content = receipt_content
    db.session.add(receipt_data)
    db.session.commit()
    return receipt_data.id


def count_receipts():
    return ReceiptData.query.all().count()

def save_products(products: dict[str, float], receipt_id: int):
    for product_name, price in products.items():
        product = Product(name=product_name, price=price, receipt_id=receipt_id)
        db.session.add(product)

    db.session.commit()
