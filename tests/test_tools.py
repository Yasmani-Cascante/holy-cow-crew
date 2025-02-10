import pytest
from datetime import datetime
import pandas as pd
from src.tools.prediction_tools import PredictionTools
from src.models.inventory_models import InventoryItem

def test_prediction_tools():
    tools = PredictionTools()
    assert len(tools.get_tools()) > 0