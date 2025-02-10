import pytest
from typing import Dict, Any, List
from datetime import datetime
from src.integrator import HolyCowIntegrator

@pytest.fixture
def integrator():
    return HolyCowIntegrator()

def test_integrator_initialization(integrator):
    state = integrator.get_system_state()
    assert state['health_status'] == 'operational'

def test_analyze_location(integrator):
    result = integrator.analyze_location({'location': 'Zurich'})
    assert result['location'] == 'Zurich'

def test_system_health_monitoring(integrator):
    state = integrator.get_system_state()
    assert 'health_status' in state

def test_error_handling(integrator):
    with pytest.raises(Exception):
        integrator.analyze_location({})