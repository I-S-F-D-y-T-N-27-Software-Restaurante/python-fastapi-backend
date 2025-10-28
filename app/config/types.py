from enum import Enum


class Roles(str, Enum):
    WAITER = "waiter"
    COOK = "cook"
    CASHIER = "cashier"
    ADMIN = "admin"


class OrderStatus(str, Enum):
    UNASSIGNED = "unassigned"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELED = "canceled"


class RestaurantTableStatus(str, Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    CLEANING = "cleaning"
    MAINTENANCE = "maintenance"
