from models.product import Product
from models.supplier import Supplier

class ProductService:

    @staticmethod
    def get_products():
        return Product.get_all()

    @staticmethod
    def get_by_id(product_id):
        return Product.get_by_id(product_id)

    @staticmethod
    def add_product(name, category, size, color, price, stock, description, import_price=0, supplier_name=""):
        if supplier_name:
            Supplier.get_or_create(supplier_name)
        Product.create(name, category, size, color, price, stock, description, import_price, supplier_name)

    @staticmethod
    def update_product(product_id, name, category, size, color, price, stock, description, import_price=0, supplier_name=""):
        if supplier_name:
            Supplier.get_or_create(supplier_name)
        Product.update(product_id, name, category, size, color, price, stock, description, import_price, supplier_name)

    @staticmethod
    def delete_product(product_id):
        Product.delete(product_id)

    @staticmethod
    def search_product(keyword):
        return Product.search(keyword)