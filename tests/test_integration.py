import pytest
from typing import Dict, Any, List
from datetime import datetime
from src.integrator import HolyCowIntegrator

@pytest.fixture
def integrator():
    return HolyCowIntegrator()

def test_location_analysis(integrator):
    result = integrator.analyze_location({'location': 'Zurich'})
    assert result['location'] == 'Zurich'

def test_efficiency_metrics(integrator):
    result = integrator.analyze_location({'location': 'Zurich'})
    assert 'resource_optimization' in result

def test_resource_optimization_integration(integrator):
    result = integrator.analyze_location({'location': 'Zurich'})
    assert 'resource_optimization' in result

def test_critical_alerts_integration(integrator):
    alerts = integrator.get_active_alerts()
    assert isinstance(alerts, list)

def test_error_handling(integrator):
    with pytest.raises(Exception):
        integrator.analyze_location({})

def test_state_persistence(integrator):
    state = integrator.get_system_state()
    assert 'health_status' in state