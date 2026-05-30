from models.customer import Customer


class CustomerService:

    @staticmethod
    def get_customers():

        return Customer.get_all()
    @staticmethod
    def add_customer(
            full_name,
            phone,
            email,
            points,
            member_rank
    ):

        Customer.create(
            full_name,
            phone,
            email,
            points,
            member_rank
        )

    @staticmethod
    def update_customer(
            customer_id,
            full_name,
            phone,
            email,
            points,
            member_rank
    ):

        Customer.update(
            customer_id,
            full_name,
            phone,
            email,
            points,
            member_rank
        )
    @staticmethod
    def delete_customer(customer_id):

        Customer.delete(customer_id)

    @staticmethod
    def search_customer(keyword):

        return Customer.search(keyword)

    @staticmethod
    def get_purchase_history(customer_name):
        return Customer.get_purchase_history(customer_name)