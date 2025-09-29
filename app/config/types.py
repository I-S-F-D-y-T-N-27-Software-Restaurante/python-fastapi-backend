from enum import Enum


class UserProfileEnum(str, Enum):
    WAITER = "waiter"
    COOK = "cook"
    CASHIER = "cashier"
