import pytest
from typing import Dict, Any, List
from datetime import datetime
from src.agents.market_strategy_agent import MarketStrategyAgent

@pytest.fixture
def agent():
    return MarketStrategyAgent()

def test_agent_creation(agent):
    assert agent.get_agent() is not None

def test_analyze_market():
    pass  # Implementar cuando MarketStrategyAgent esté listo