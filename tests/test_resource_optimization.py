import pytest
from datetime import datetime
from src.models.inventory_models import (
    InventoryItem,
    InventoryLevel,
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
def sample_levels():
    return {
        'BEEF001': InventoryLevel(
            item_id="BEEF001",
            current_quantity=200,
            reserved_quantity=20,
            available_quantity=180,
            last_updated=datetime.now()
        )
    }

@pytest.fixture
def sample_predictions():
    return {
        'BEEF001': InventoryPrediction(
            predicted_demand=100.0,
            confidence_range=(80.0, 120.0),
            trend_factor=1.1,
            seasonality_factor=1.0
        )
    }

def test_basic_functionality(sample_items, sample_levels, sample_predictions):
    assert len(sample_items) > 0
    assert len(sample_levels) > 0
    assert len(sample_predictions) > 0