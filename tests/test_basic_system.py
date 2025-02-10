import pytest
from typing import Dict, Any, List
from datetime import datetime
from src.agents.performance_analysis_agent import PerformanceAnalysisAgent
import pandas as pd

def test_performance_agent_basic():
    agent = PerformanceAnalysisAgent()
    result = agent.analyze_sales_data({
        'historical_data': pd.DataFrame(),
        'location': 'Zurich'
    })
    assert 'predictions' in result