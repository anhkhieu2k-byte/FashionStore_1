import bcrypt

from models.account import Account

username = "admin"

password = "123456"

hashed_password = bcrypt.hashpw(
    password.encode(),
    bcrypt.gensalt()
)

Account.create_account(
    username,
    hashed_password,
    "Admin"
)

print("Admin created!")