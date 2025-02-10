import pytest
from datetime import datetime
from src.tools.inventory_tools import InventoryTools
from src.models.inventory_models import (
    InventoryItem,
    InventoryLevel,
    BatchInfo
)

@pytest.fixture
def sample_item():
    return InventoryItem(
        id="BEEF001",
        name="Swiss Beef Patty",
        category="MEAT",
        storage="REFRIGERATED",
        unit="piece",
        min_level=150,
        max_level=600,
        reorder_point=250,
        lead_time_days=2,
        shelf_life_days=4,
        cost_per_unit=4.50,
        supplier_id="SWISS_MEAT"
    )

@pytest.fixture
def sample_inventory_level():
    return InventoryLevel(
        item_id="BEEF001",
        current_quantity=200,
        reserved_quantity=20,
        available_quantity=180,
        last_updated=datetime.now(),
        batch_info=[
            BatchInfo(
                batch_id="B001",
                quantity=200,
                expiry_date=datetime.now()
            )
        ]
    )

def test_analyze_inventory_levels(sample_item, sample_inventory_level):
    tools = InventoryTools()
    
    result = tools.analyze_inventory_levels(
        current_levels={"BEEF001": sample_inventory_level},
        items={"BEEF001": sample_item},
        historical_movements=[],
        predicted_sales=1000
    )
    
    assert isinstance(result, dict)
    assert "BEEF001" in result

def test_inventory_alerts(sample_item, sample_inventory_level):
    tools = InventoryTools()
    
    low_stock_level = InventoryLevel(
        item_id="BEEF001",
        current_quantity=100,
        reserved_quantity=0,
        available_quantity=100,
        last_updated=datetime.now()
    )
    
    result = tools.analyze_inventory_levels(
        current_levels={"BEEF001": low_stock_level},
        items={"BEEF001": sample_item},
        historical_movements=[],
        predicted_sales=1000
    )
    
    assert "BEEF001" in result