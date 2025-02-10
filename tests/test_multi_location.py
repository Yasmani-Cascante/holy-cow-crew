import pytest
from datetime import datetime
from src.tools.multi_location_tools import MultiLocationTools
from src.models.inventory_models import (
    InventoryItem,
    InventoryPrediction
)

@pytest.fixture
def sample_items():
    return {
        'BEEF001': InventoryItem(
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
    }

@pytest.fixture
def sample_inventory():
    return {
        'Zurich': {'BEEF001': 200},
        'Geneva': {'BEEF001': 400},
        'Basel': {'BEEF001': 150}
    }

@pytest.fixture
def sample_predictions():
    prediction = InventoryPrediction(
        predicted_demand=100,
        confidence_range=(80, 120),
        trend_factor=1.1,
        seasonality_factor=1.0
    )
    return {
        location: {'BEEF001': prediction}
        for location in ['Zurich', 'Geneva', 'Basel']
    }

def test_optimize_orders(sample_inventory, sample_predictions, sample_items):
    tools = MultiLocationTools()
    
    recommendations = tools.optimize_orders(
        locations_inventory=sample_inventory,
        demand_predictions=sample_predictions,
        items=sample_items
    )
    
    assert 'Zurich' in recommendations
    zurich_rec = recommendations['Zurich']
    assert isinstance(zurich_rec.new_orders, dict)
    assert isinstance(zurich_rec.transfers_in, dict)

def test_transfer_cost():
    tools = MultiLocationTools()
    item = InventoryItem(
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
    
    cost = tools._calculate_transfer_cost(
        'Zurich',
        'Geneva',
        100,
        item
    )
    
    assert cost > 0
    assert isinstance(cost, float)