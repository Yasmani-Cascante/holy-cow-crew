import pytest
from src.agents.performance_analysis_agent import PerformanceAnalysisAgent
from src.agents.market_strategy_agent import MarketStrategyAgent

def test_performance_agent_basic():
    agent = PerformanceAnalysisAgent()
    
    test_data = {
        'predicted_value': 1000,
        'confidence_interval': (900, 1100),
        'capacity': 100,
        'historical_data': {
            'predicted': [100, 150, 200],
            'actual': [110, 160, 190]
        }
    }
    
    result = agent.analyze_sales_data(test_data)
    
    try:
        assert 'uncertainty_level' in result
        assert 'capacity_utilization' in result
        assert 'insights' in result
        assert 'metrics' in result
    except AssertionError as e:
        raise AssertionError(f"Error en análisis básico: {e}")

def test_market_strategy_basic():
    agent = MarketStrategyAgent()
    result = agent.develop_local_strategy("Zurich", "2024-02-01", "2024-02-28")
    
    assert 'events' in result
    assert 'demographics' in result
    assert 'recommendations' in result