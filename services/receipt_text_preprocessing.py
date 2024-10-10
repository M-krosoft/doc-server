from re import findall

class ReceiptTextPreprocessingService:
    def __init__(self):
        pass

    @staticmethod
    def _get_pattern_for_searching_products() -> str:
        product_name_pattern = r"([A-Za-z ]+)"
        optional_numbers_pattern = r"(\d+[.,]\d*\*\d+[.,]\d*?)?"
        price_pattern = r"(\d+[.,]\d*)[A-F]"

        pattern = product_name_pattern + optional_numbers_pattern + "\n" + optional_numbers_pattern +  price_pattern
        return pattern

    def filter_text_from_receipt(self, receipt_as_text: str) -> list[tuple[str, str, str, str]]:
        pattern = self._get_pattern_for_searching_products()
        products_information = findall(pattern, receipt_as_text)
        return products_information

    @staticmethod
    def process_products_information_to_dict(products_information: list[tuple[str, str, str, str]]) -> dict[str, float]:
        products_with_prices = dict()
        for product in products_information:
            if product[0] and product[3]:
                try:
                    products_with_prices[product[0]] = float(product[3])
                except ValueError:
                    products_with_prices[product[0]] = -1.0
        return products_with_prices

    def get_products_with_prices(self, receipt_as_text: str) -> dict[str, float]:
        products_information = self.filter_text_from_receipt(receipt_as_text)
        return self.process_products_information_to_dict(products_information)