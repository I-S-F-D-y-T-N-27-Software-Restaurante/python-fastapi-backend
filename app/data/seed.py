from app.config.types import Roles
from app.resto.services import get_employee_by_email, make_user_role
from app.user.dto import UserCreateDTO
from app.user.services import create_user, hard_wipe_users


def seed(should_wipe: bool):
    if should_wipe:
        hard_wipe_users()

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

        make_user_role(alice, role=Roles.WAITER)
        make_user_role(bob, role=Roles.WAITER)

        make_user_role(alice, role=Roles.COOK)
        make_user_role(charlie, role=Roles.COOK)

        make_user_role(alice, role=Roles.CASHIER)
        make_user_role(diana, role=Roles.CASHIER)

    except Exception:
        print("Ignoring error during seed role assignment")
