import pytest
import pandas as pd
from datetime import datetime
from src.tools.demand_prediction_tools import DemandPredictionTools
from src.models.inventory_models import InventoryItem

@pytest.fixture
def sample_historical_data():
    return pd.DataFrame({
        'date': ['2024-11-01', '2024-11-15', '2024-11-30'],
        'location': ['Zurich'] * 3,
        'item_id': ['BEEF001'] * 3,
        'units_sold': [120, 135, 140],
        'waste_units': [2, 3, 2]
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

def test_predict_demand(sample_historical_data, sample_items):
    tools = DemandPredictionTools()
    
    predictions = tools.predict_demand(
        historical_data=sample_historical_data,
        items=sample_items,
        target_date=datetime.now(),
        location='Zurich'
    )
    
    assert 'BEEF001' in predictions
    prediction = predictions['BEEF001']
    assert prediction.predicted_demand > 0
    assert prediction.confidence_range[0] < prediction.confidence_range[1]
    assert 0.5 <= prediction.trend_factor <= 1.5

def test_calculate_trend(sample_historical_data):
    tools = DemandPredictionTools()
    trend = tools._calculate_trend(sample_historical_data)
    assert 0.5 <= trend <= 1.5