import pytest
from datetime import datetime
from src.tools.market_tools import MarketTools
from src.models.market_models import LocalEvent, CantonInfo, MarketingRecommendation

@pytest.fixture
def market_tools():
    return MarketTools()

def test_analyze_local_events(market_tools):
    # Test period covering known events
    date_range = ('2025-06-01', '2025-08-31')
    events = market_tools.analyze_local_events('Zurich', date_range)
    
    assert len(events) >= 1
    event = events[0]
    assert isinstance(event, LocalEvent)
    assert hasattr(event, 'name')
    assert hasattr(event, 'expected_attendance')

def test_analyze_canton_demographics(market_tools):
    demographics = market_tools.analyze_canton_demographics('Zurich')
    
    assert isinstance(demographics, CantonInfo)
    assert demographics.language == 'German'
    assert demographics.population > 0
    assert len(demographics.key_demographics) > 0

def test_generate_recommendations(market_tools):
    # Test data
    events = [
        LocalEvent(
            name='Test Event',
            date='2025-07-01',
            location='Zurich',
            expected_attendance=50000,
            category='cultural'
        )
    ]
    
    demographics = CantonInfo(
        name='Zurich',
        language='German',
        population=1500000,
        key_demographics={'young_professionals': 0.35}
    )
    
    recommendations = market_tools.generate_recommendations(events, demographics)
    
    assert len(recommendations) > 0
    assert isinstance(recommendations[0], MarketingRecommendation)
    assert recommendations[0].target_location == 'Zurich'

def test_invalid_canton(market_tools):
    with pytest.raises(ValueError):
        market_tools.analyze_canton_demographics('InvalidCanton')

def test_empty_date_range(market_tools):
    date_range = ('2025-01-01', '2025-01-31')  # Period with no known events
    events = market_tools.analyze_local_events('Zurich', date_range)
    assert len(events) == 0

def test_get_tools(market_tools):
    tools = market_tools.get_tools()
    assert len(tools) == 3
    tool_names = {tool.name for tool in tools}
    assert 'analyze_local_events' in tool_names
    assert 'analyze_canton_demographics' in tool_names
    assert 'generate_recommendations' in tool_names