from models.promotion import Promotion


class PromotionService:

    @staticmethod
    def get_promotions():

        return Promotion.get_all()

    @staticmethod
    def add_promotion(
            code,
            discount_percent,
            min_order_value,
            start_date,
            end_date,
            quantity=999
    ):

        Promotion.create(
            code,
            discount_percent,
            min_order_value,
            start_date,
            end_date,
            quantity
        )

    @staticmethod
    def update_promotion(
            promotion_id,
            code,
            discount_percent,
            min_order_value,
            start_date,
            end_date,
            quantity=999
    ):

        Promotion.update(
            promotion_id,
            code,
            discount_percent,
            min_order_value,
            start_date,
            end_date,
            quantity
        )

    @staticmethod
    def delete_promotion(promotion_id):

        Promotion.delete(promotion_id)

    @staticmethod
    def search_promotion(keyword):

        return Promotion.search(keyword)

    @staticmethod
    def get_by_code(code):
        return Promotion.get_by_code(code)

    @staticmethod
    def check_customer_usage(customer_name, code):
        return Promotion.check_customer_usage(customer_name, code)

    @staticmethod
    def increment_used_count(code):
        Promotion.increment_used_count(code)