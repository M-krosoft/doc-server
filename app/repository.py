from app import db
from app.model import ReceiptData, Product


def save_receipt(receipt_content: str) -> int:
    receipt_data = ReceiptData()
    receipt_data.content = receipt_content
    db.session.add(receipt_data)
    db.session.commit()
    return receipt_data.id


def count_receipts() -> int:
    return ReceiptData.query.all().count()

def save_products(products: dict[str, float], receipt_id: int) -> None:
    for product_name, price in products.items():
        product = Product(name=product_name, price=price, receipt_id=receipt_id)
        db.session.add(product)

    db.session.commit()

def get_products_with_prices_by_receipt_id(receipt_id: int) -> dict[str, float]:
    products_with_prices = {}
    receipt = ReceiptData.query.get(receipt_id)

    if receipt:
        for product in receipt.products:
            products_with_prices[product.name] = product.price
    return products_with_prices
