from src.models.inventory_models import (
    InventoryItem,
    ItemCategory,
    StorageCondition
)

INVENTORY_ITEMS = {
    # Panes
    "BUN001": InventoryItem(
        id="BUN001",
        name="Classic Burger Buns",
        category=ItemCategory.PERISHABLE,
        storage=StorageCondition.ROOM_TEMP,
        unit="piece",
        min_level=200,
        max_level=800,
        reorder_point=300,
        lead_time_days=2,
        shelf_life_days=5,
        cost_per_unit=0.75,
        supplier_id="LOCAL_BAKERY"
    ),
    
    # Carnes y alternativas
    "BEEF001": InventoryItem(
        id="BEEF001",
        name="Swiss Beef Patty 180g",
        category=ItemCategory.PERISHABLE,
        storage=StorageCondition.REFRIGERATED,
        unit="piece",
        min_level=150,
        max_level=600,
        reorder_point=250,
        lead_time_days=2,
        shelf_life_days=4,
        cost_per_unit=4.50,
        supplier_id="SWISS_MEAT"
    ),
    "BEEF002": InventoryItem(
        id="BEEF002",
        name="Plant-Based Patty",
        category=ItemCategory.FROZEN,
        storage=StorageCondition.FROZEN,
        unit="piece",
        min_level=50,
        max_level=200,
        reorder_point=75,
        lead_time_days=4,
        shelf_life_days=90,
        cost_per_unit=5.20,
        supplier_id="VEGAN_SUPPLIES"
    ),
    
    # Quesos
    "CHEESE001": InventoryItem(
        id="CHEESE001",
        name="Raclette Cheese",
        category=ItemCategory.PERISHABLE,
        storage=StorageCondition.REFRIGERATED,
        unit="kg",
        min_level=5,
        max_level=20,
        reorder_point=8,
        lead_time_days=3,
        shelf_life_days=14,
        cost_per_unit=22.00,
        supplier_id="SWISS_DAIRY"
    ),
    
    # Verduras
    "VEG001": InventoryItem(
        id="VEG001",
        name="Fresh Lettuce",
        category=ItemCategory.PERISHABLE,
        storage=StorageCondition.REFRIGERATED,
        unit="head",
        min_level=30,
        max_level=100,
        reorder_point=40,
        lead_time_days=1,
        shelf_life_days=5,
        cost_per_unit=1.20,
        supplier_id="LOCAL_PRODUCE"
    ),
    "VEG002": InventoryItem(
        id="VEG002",
        name="Tomatoes",
        category=ItemCategory.PERISHABLE,
        storage=StorageCondition.ROOM_TEMP,
        unit="kg",
        min_level=10,
        max_level=30,
        reorder_point=15,
        lead_time_days=1,
        shelf_life_days=5,
        cost_per_unit=3.50,
        supplier_id="LOCAL_PRODUCE"
    ),
    
    # Salsas
    "SAUCE001": InventoryItem(
        id="SAUCE001",
        name="Holy Sauce",
        category=ItemCategory.PERISHABLE,
        storage=StorageCondition.REFRIGERATED,
        unit="liter",
        min_level=5,
        max_level=20,
        reorder_point=8,
        lead_time_days=3,
        shelf_life_days=14,
        cost_per_unit=8.00,
        supplier_id="HOLY_COW_CENTRAL"
    ),
    "SAUCE002": InventoryItem(
        id="SAUCE002",
        name="BBQ Sauce",
        category=ItemCategory.PERISHABLE,
        storage=StorageCondition.REFRIGERATED,
        unit="liter",
        min_level=4,
        max_level=15,
        reorder_point=6,
        lead_time_days=3,
        shelf_life_days=14,
        cost_per_unit=7.50,
        supplier_id="HOLY_COW_CENTRAL"
    ),
    
    # Complementos
    "COMP001": InventoryItem(
        id="COMP001",
        name="Truffle Mayo",
        category=ItemCategory.PERISHABLE,
        storage=StorageCondition.REFRIGERATED,
        unit="liter",
        min_level=2,
        max_level=8,
        reorder_point=3,
        lead_time_days=4,
        shelf_life_days=14,
        cost_per_unit=24.00,
        supplier_id="SPECIALTY_FOODS"
    ),
    
    # Papas
    "FRIES001": InventoryItem(
        id="FRIES001",
        name="Premium Fries",
        category=ItemCategory.FROZEN,
        storage=StorageCondition.FROZEN,
        unit="kg",
        min_level=50,
        max_level=200,
        reorder_point=75,
        lead_time_days=3,
        shelf_life_days=180,
        cost_per_unit=3.20,
        supplier_id="FROZEN_FOODS"
    ),
    
    # Empaque
    "SUP001": InventoryItem(
        id="SUP001",
        name="Eco-Friendly Packaging",
        category=ItemCategory.SUPPLIES,
        storage=StorageCondition.ROOM_TEMP,
        unit="piece",
        min_level=500,
        max_level=2000,
        reorder_point=750,
        lead_time_days=5,
        shelf_life_days=None,
        cost_per_unit=0.45,
        supplier_id="ECO_SUPPLIES"
    )
}

# Recetas de las hamburguesas
BURGER_RECIPES = {
    "CLASSIC": {
        "BUN001": 1,      # Classic Bun
        "BEEF001": 1,     # Swiss Beef Patty
        "VEG001": 0.1,    # Lettuce
        "VEG002": 0.08,   # Tomatoes
        "SAUCE001": 0.03, # Holy Sauce
        "SUP001": 1,      # Eco Packaging
    },
    "VEGGIE": {
        "BUN001": 1,      # Classic Bun
        "BEEF002": 1,     # Plant-Based Patty
        "VEG001": 0.15,   # Extra Lettuce
        "VEG002": 0.1,    # Tomatoes
        "SAUCE001": 0.03, # Holy Sauce
        "SUP001": 1,      # Eco Packaging
    },
    "CHEESE_LOVER": {
        "BUN001": 1,      # Classic Bun
        "BEEF001": 1,     # Swiss Beef Patty
        "CHEESE001": 0.05,# Raclette
        "SAUCE001": 0.03, # Holy Sauce
        "SUP001": 1,      # Eco Packaging
    },
    "TRUFFLE": {
        "BUN001": 1,      # Classic Bun
        "BEEF001": 1,     # Swiss Beef Patty
        "CHEESE001": 0.05,# Raclette
        "COMP001": 0.04,  # Truffle Mayo
        "SUP001": 1,      # Eco Packaging
    }
}