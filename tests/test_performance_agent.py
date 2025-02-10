import pytest
from typing import Dict, Any, List
from datetime import datetime
import pandas as pd
from src.agents.performance_analysis_agent import PerformanceAnalysisAgent

@pytest.fixture
def agent():
    return PerformanceAnalysisAgent()

def test_agent_creation(agent):
    assert agent.get_agent() is not None

def test_agent_has_tools(agent):
    assert len(agent.tools.get_tools()) > 0

def test_analyze_sales_data(agent):
    result = agent.analyze_sales_data({
        'historical_data': pd.DataFrame(),
        'location': 'Zurich'
    })
    assert 'predictions' in result