import pytest
from src.tools.prediction_tools import (
    PredictionTools, 
    PredictionAnalysisInput,
    MetricsCalculationInput
)

def test_analyze_prediction():
    tools = PredictionTools()
    
    # Test data
    input_data = PredictionAnalysisInput(
        predicted_value=1000,
        confidence_interval=(900, 1100),
        capacity=100
    )
    
    result = tools.analyze_prediction(input_data)
    
    # Verify result structure
    assert 'uncertainty_level' in result
    assert 'capacity_utilization' in result
    assert 'insights' in result
    assert 'timestamp' in result
    
    # Verify calculations
    assert 0 <= result['uncertainty_level'] <= 1
    assert 0 <= result['capacity_utilization'] <= 100
    assert isinstance(result['insights'], list)
    
def test_calculate_metrics():
    tools = PredictionTools()
    
    # Test data
    input_data = MetricsCalculationInput(
        predicted=[100, 150, 200],
        actual=[110, 160, 190]
    )
    
    result = tools.calculate_metrics(input_data)
    
    # Verify result structure
    assert 'mae' in result
    assert 'mape' in result
    assert 'accuracy' in result
    assert 'sample_size' in result
    
    # Verify calculations
    assert result['mae'] > 0
    assert 0 <= result['accuracy'] <= 100
    assert result['sample_size'] == len(input_data.predicted)

def test_analyze_prediction_edge_cases():
    tools = PredictionTools()
    
    # Test with zero predicted value
    with pytest.raises(ZeroDivisionError):
        input_data = PredictionAnalysisInput(
            predicted_value=0,
            confidence_interval=(0, 0),
            capacity=100
        )
        tools.analyze_prediction(input_data)

def test_calculate_metrics_empty_lists():
    tools = PredictionTools()
    
    with pytest.raises(ValueError):
        input_data = MetricsCalculationInput(
            predicted=[],
            actual=[]
        )
        tools.calculate_metrics(input_data)

def test_get_tools():
    tools = PredictionTools()
    tool_list = tools.get_tools()
    
    assert len(tool_list) == 2
    assert all(hasattr(tool, 'name') for tool in tool_list)
    assert all(hasattr(tool, 'description') for tool in tool_list)