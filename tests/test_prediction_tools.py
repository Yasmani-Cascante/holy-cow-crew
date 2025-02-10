import pytest
from datetime import datetime
import pandas as pd
from src.tools.prediction_tools import PredictionTools
from src.models.inventory_models import InventoryItem

@pytest.fixture
def tools():
    return PredictionTools()

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'item_id': ['BEEF001'],
        'units_sold': [100]
    })

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

def test_predict_demand(tools, sample_data, sample_items):
    predictions = tools.predict_demand(
        historical_data=sample_data,
        items=sample_items,
        target_date=datetime.now(),
        location='Zurich'
    )
    assert 'BEEF001' in predictions
    assert predictions['BEEF001'].predicted_demand > 0

def test_prediction_tools_structure(tools):
    tool_list = tools.get_tools()
    assert len(tool_list) > 0
    assert tool_list[0].name == "predict_demand"