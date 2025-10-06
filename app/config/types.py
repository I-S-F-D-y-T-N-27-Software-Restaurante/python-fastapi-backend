from enum import Enum


class Roles(str, Enum):
    WAITER = "waiter"
    COOK = "cook"
    CASHIER = "cashier"
    ADMIN = "admin"
