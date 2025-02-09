import pytest
from src.tools.marketing_tools import MarketingTools

def test_analyze_local_events():
    tools = MarketingTools()
    events = tools.analyze_local_events("Zurich", ["2024-02-01", "2024-02-28"])
    
    assert isinstance(events, list)
    if events:
        assert "name" in events[0]
        assert "date" in events[0]
        assert "expected_attendance" in events[0]

def test_analyze_canton_demographics():
    tools = MarketingTools()
    demographics = tools.analyze_canton_demographics("Zurich")
    
    assert isinstance(demographics, dict)
    assert "name" in demographics
    assert "population" in demographics
    assert "key_demographics" in demographics

def test_generate_recommendations():
    tools = MarketingTools()
    events = tools.analyze_local_events("Zurich", ["2024-02-01", "2024-02-28"])
    demographics = tools.analyze_canton_demographics("Zurich")
    
    recommendations = tools.generate_recommendations(events, demographics)
    
    assert isinstance(recommendations, dict)
    assert "target_segments" in recommendations
    assert "channels" in recommendations
    assert "tactics" in recommendations