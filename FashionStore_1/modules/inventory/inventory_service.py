from models.inventory import Inventory


class InventoryService:

    @staticmethod
    def get_inventory():

        return Inventory.get_all()

    @staticmethod
    def add_inventory(
            product_name,
            quantity,
            min_quantity,
            supplier_name,
            import_price
    ):

        Inventory.create(
            product_name,
            quantity,
            min_quantity,
            supplier_name,
            import_price
        )

    @staticmethod
    def update_inventory(
            inventory_id,
            product_name,
            quantity,
            min_quantity,
            supplier_name,
            import_price
    ):

        Inventory.update(
            inventory_id,
            product_name,
            quantity,
            min_quantity,
            supplier_name,
            import_price
        )

    @staticmethod
    def delete_inventory(inventory_id):

        Inventory.delete(inventory_id)

    @staticmethod
    def search_inventory(keyword):

        return Inventory.search(keyword)