import pytest
from src.agents.performance_analysis_agent import PerformanceAnalysisAgent

def test_agent_creation():
    agent = PerformanceAnalysisAgent()
    assert agent.get_agent() is not None

def test_agent_has_tools():
    agent = PerformanceAnalysisAgent()
    crew_agent = agent.get_agent()
    assert hasattr(crew_agent, 'tools')
    assert len(crew_agent.tools) > 0

def test_analyze_sales_data():
    agent = PerformanceAnalysisAgent()
    
    # Test data
    prediction_data = {
        'predicted_value': 1000,
        'confidence_interval': (900, 1100),
        'capacity': 100,
        'historical_data': {
            'predicted': [100, 150, 200],
            'actual': [110, 160, 190]
        }
    }
    
    result = agent.analyze_sales_data(prediction_data)
    
    # Verify analysis results
    assert 'uncertainty_level' in result
    assert 'capacity_utilization' in result
    assert 'insights' in result
    assert 'metrics' in result
    
    # Verify metrics
    metrics = result['metrics']
    assert 'mae' in metrics
    assert 'mape' in metrics
    assert 'accuracy' in metrics