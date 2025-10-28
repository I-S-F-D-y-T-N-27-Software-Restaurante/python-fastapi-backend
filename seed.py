from app.config.types import Roles
from app.resto.services import make_user_role
from app.user.dto import UserCreateDTO
from app.user.services import create_user, get_user_by_email, hard_wipe_users


def seed(should_wipe: bool):
    if should_wipe:
        hard_wipe_users()

    seed_users = [
        {"name": "Alice", "email": "alice@example.com", "password": "pass123"},
        {"name": "Bob", "email": "bob@example.com", "password": "pass123"},
        {"name": "Charlie", "email": "charlie@example.com", "password": "pass123"},
        {"name": "Diana", "email": "diana@example.com", "password": "pass123"},
        {"name": "Evan", "email": "evan@example.com", "password": "pass123"},
    ]

    for user_data in seed_users:
        if not get_user_by_email(user_data["email"]):
            user_dto = UserCreateDTO(**user_data)
            create_user(user_dto)

    try:
        alice = get_user_by_email("alice@example.com")
        bob = get_user_by_email("bob@example.com")
        charlie = get_user_by_email("charlie@example.com")
        diana = get_user_by_email("diana@example.com")

        if alice:
            make_user_role(alice, role=Roles.CASHIER)
            make_user_role(alice, role=Roles.WAITER)
            make_user_role(alice, role=Roles.COOK)

        if bob:
            make_user_role(bob, role=Roles.WAITER)

        if charlie:
            make_user_role(charlie, role=Roles.COOK)

        if diana:
            make_user_role(diana, role=Roles.CASHIER)

        

    except Exception as e:
        print("Error during seed: ", e)


if __name__ == "__main__":
    seed(True)
