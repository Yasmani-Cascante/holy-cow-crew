import pytest
from typing import Dict, Any, List
from datetime import datetime
from src.agents.resource_optimization_agent import ResourceOptimizationAgent
from src.models.inventory_models import (
    InventoryItem,
    InventoryLevel,
    LocationRecommendation,
    OrderRecommendation,
    TransferOption
)

@pytest.fixture
def sample_inventory_items():
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
def sample_inventory_levels():
    return {
        'Zurich': {
            'BEEF001': InventoryLevel(
                item_id="BEEF001",
                current_quantity=200,
                reserved_quantity=0,
                available_quantity=200,
                last_updated=datetime.now()
            )
        }
    }

@pytest.fixture
def sample_data(sample_inventory_levels, sample_inventory_items):
    return {
        'locations': ['Zurich', 'Geneva'],
        'historical_data_path': 'data/sample/inventory_data.csv',
        'inventory_levels': sample_inventory_levels,
        'inventory_items': sample_inventory_items
    }

def test_agent_creation():
    agent = ResourceOptimizationAgent()
    assert agent.get_agent() is not None

def test_create_optimization_task():
    agent = ResourceOptimizationAgent()
    task = agent.create_optimization_task('Zurich')
    assert task.description is not None
    assert 'Zurich' in task.description