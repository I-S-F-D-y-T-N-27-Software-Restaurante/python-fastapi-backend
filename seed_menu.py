from decimal import Decimal

from app.menu.dto import CreateMenuItemDTO
from app.menu.services import create_menu_entries, hard_delete_all_menu_items

menu_seed = [
    CreateMenuItemDTO(
        name="Bruschetta",
        description="Pan tostado con tomate y albahaca",
        price=Decimal("5.50"),
        category="entrada",
    ),
    CreateMenuItemDTO(
        name="Empanadas de Carne",
        description="Empanadas rellenas de carne con especias",
        price=Decimal("6.00"),
        category="entrada",
    ),
    CreateMenuItemDTO(
        name="Sopa de Verduras",
        description="Sopa caliente de verduras de temporada",
        price=Decimal("7.00"),
        category="sopa",
    ),
    CreateMenuItemDTO(
        name="Ensalada Cesar",
        description="Lechuga romana con aderezo Cesar y crutones",
        price=Decimal("8.50"),
        category="ensalada",
    ),
    CreateMenuItemDTO(
        name="Pollo al Horno",
        description="Pollo asado al horno con hierbas",
        price=Decimal("15.00"),
        category="plato_principal",
    ),
    CreateMenuItemDTO(
        name="Pasta Alfredo",
        description="Pasta cremosa con salsa Alfredo y parmesano",
        price=Decimal("14.00"),
        category="plato_principal",
    ),
    CreateMenuItemDTO(
        name="Lasana de Carne",
        description="Lasana con capas de carne, pasta y queso",
        price=Decimal("16.00"),
        category="plato_principal",
    ),
    CreateMenuItemDTO(
        name="Pizza Margherita",
        description="Pizza clasica con tomate, mozzarella y albahaca",
        price=Decimal("12.50"),
        category="plato_principal",
    ),
    CreateMenuItemDTO(
        name="Pizza Pepperoni",
        description="Pizza con pepperoni y mozzarella",
        price=Decimal("13.50"),
        category="plato_principal",
    ),
    CreateMenuItemDTO(
        name="Helado de Vainilla",
        description="Bola de helado de vainilla",
        price=Decimal("5.00"),
        category="postre",
    ),
    CreateMenuItemDTO(
        name="Brownie de Chocolate",
        description="Brownie de chocolate con nueces",
        price=Decimal("6.50"),
        category="postre",
    ),
    CreateMenuItemDTO(
        name="Tarta de Frutillas",
        description="Tarta de frutillas con crema",
        price=Decimal("6.00"),
        category="postre",
    ),
    CreateMenuItemDTO(
        name="Agua Mineral",
        description="Botella de agua mineral",
        price=Decimal("3.00"),
        category="bebida",
    ),
    CreateMenuItemDTO(
        name="Jugo Natural de Naranja",
        description="Jugo de naranja recien exprimido",
        price=Decimal("4.50"),
        category="bebida",
    ),
    CreateMenuItemDTO(
        name="Gaseosa Cola",
        description="Gaseosa de cola 500ml",
        price=Decimal("4.00"),
        category="bebida",
    ),
    CreateMenuItemDTO(
        name="Papas Fritas",
        description="Papas fritas crujientes",
        price=Decimal("5.00"),
        category="acompanamiento",
    ),
    CreateMenuItemDTO(
        name="Arroz Pilaf",
        description="Arroz pilaf sazonado",
        price=Decimal("4.50"),
        category="acompanamiento",
    ),
    CreateMenuItemDTO(
        name="Nachos con Queso",
        description="Totopos con queso derretido",
        price=Decimal("6.50"),
        category="snack",
    ),
    CreateMenuItemDTO(
        name="Alitas BBQ",
        description="Alitas de pollo con salsa BBQ",
        price=Decimal("9.00"),
        category="snack",
    ),
    CreateMenuItemDTO(
        name="Filete Especial del Chef",
        description="Filete especial a la parrilla del chef",
        price=Decimal("20.00"),
        category="especial",
    ),
]


def seed_menu():
    try:
        hard_delete_all_menu_items()
        created_items = create_menu_entries(menu_seed)
        print(f"Seeded {len(created_items)} menu items successfully.")
    except Exception as e:
        print(f"Error seeding menu items: {e}")


if __name__ == "__main__":
    seed_menu()
