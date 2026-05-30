from database.db_connect import get_connection

class Account:
    @staticmethod
    def get_by_username(username):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM accounts
        WHERE username = ?
        """, (username,))

        account = cursor.fetchone()

        conn.close()

        return account

    @staticmethod
    def create_account(
            username,
            password,
            role
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO accounts(
            username,
            password,
            role
        )
        VALUES (?, ?, ?)
        """, (
            username,
            password,
            role
        ))

        conn.commit()

        conn.close()