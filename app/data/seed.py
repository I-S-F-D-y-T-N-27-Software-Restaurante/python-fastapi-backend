from app.config.types import UserProfileEnum
from app.resto.services import get_employee_by_email, make_user_role
from app.user.dto import UserCreateDTO
from app.user.services import create_user


def seed():
    seed_users = [
        {"name": "Alice", "email": "alice@test.com", "password": "pass123"},
        {"name": "Bob", "email": "bob@test.com", "password": "pass123"},
        {"name": "Charlie", "email": "charlie@test.com", "password": "pass123"},
        {"name": "Diana", "email": "diana@test.com", "password": "pass123"},
        {"name": "Evan", "email": "evan@test.com", "password": "pass123"},
    ]

    for user_data in seed_users:
        if not get_employee_by_email(user_data["email"]):
            user_dto = UserCreateDTO(**user_data)
            create_user(user_dto)

    try:
        alice = get_employee_by_email(seed_users[0]["email"])
        bob = get_employee_by_email(seed_users[1]["email"])
        charlie = get_employee_by_email(seed_users[2]["email"])
        diana = get_employee_by_email(seed_users[3]["email"])

        make_user_role(alice, role=UserProfileEnum.WAITER)
        make_user_role(bob, role=UserProfileEnum.WAITER)

        make_user_role(alice, role=UserProfileEnum.COOK)
        make_user_role(charlie, role=UserProfileEnum.COOK)

        make_user_role(alice, role=UserProfileEnum.CASHIER)
        make_user_role(diana, role=UserProfileEnum.CASHIER)
    except Exception:
        print("Ignoring error during role assignment")
