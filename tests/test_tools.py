import pytest
from datetime import datetime
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
    assert isinstance(result['uncertainty_level'], float)
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
    assert isinstance(result['mae'], float)
    assert 0 <= result['accuracy'] <= 100
    assert result['sample_size'] == 3

def test_get_tools():
    tools = PredictionTools()
    tool_list = tools.get_tools()
    
    assert len(tool_list) == 2  # Should have two tools
    
    # Verify tool properties
    for tool in tool_list:
        assert tool.name in ['analyze_prediction', 'calculate_metrics']
        assert isinstance(tool.description, str)
        assert callable(tool.func)

def test_edge_cases():
    tools = PredictionTools()
    
    # Test low values
    input_data = PredictionAnalysisInput(
        predicted_value=1,
        confidence_interval=(0.9, 1.1),
        capacity=10
    )
    result = tools.analyze_prediction(input_data)
    assert isinstance(result['uncertainty_level'], float)
    
    # Test high values
    input_data = PredictionAnalysisInput(
        predicted_value=10000,
        confidence_interval=(9000, 11000),
        capacity=1000
    )
    result = tools.analyze_prediction(input_data)
    assert isinstance(result['uncertainty_level'], float)

def test_error_handling():
    tools = PredictionTools()
    
    # Test with empty metrics calculation
    with pytest.raises(ValueError):
        tools.calculate_metrics(MetricsCalculationInput(
            predicted=[],
            actual=[]
        ))