import pytest
from datetime import datetime
from src.agents.market_strategy_agent import MarketStrategyAgent

def test_develop_local_strategy():
    agent = MarketStrategyAgent()
    location = "Zurich"
    start_date = datetime.now().strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    result = agent.develop_local_strategy(location, start_date, end_date)
    
    assert result is not None
    assert 'location' in result
    assert 'events' in result
    assert 'demographics' in result
    assert 'recommendations' in result