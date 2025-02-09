import pytest
from datetime import datetime
import time
from src.integrator import HolyCowIntegrator

@pytest.fixture
def integrator():
    return HolyCowIntegrator()

@pytest.fixture
def test_metrics():
    return {
        'sales_growth': {
            'current': 1000,
            'previous': 900
        },
        'staff_count': 10,
        'inventory': {
            'meat': 5.0,
            'vegetables': 3.0,
            'dairy': 4.0,
            'dry_goods': 20.0
        }
    }

def test_location_analysis(integrator, test_metrics):
    result = integrator.analyze_location("Zurich", test_metrics)
    assert result.location == "Zurich"
    assert result.performance_metrics is not None
    assert result.market_insights is not None
    assert result.resource_optimization is not None

def test_efficiency_metrics(integrator, test_metrics):
    result = integrator.analyze_location("Zurich", test_metrics)
    assert 'efficiency_score' in result.resource_optimization
    assert 0 <= result.resource_optimization['efficiency_score'] <= 100

def test_resource_optimization_integration(integrator, test_metrics):
    result = integrator.analyze_location("Zurich", test_metrics)
    assert 'recommended_staff' in result.resource_optimization
    assert 'inventory_orders' in result.resource_optimization
    assert 'alerts' in result.resource_optimization

def test_critical_alerts_integration(integrator):
    alerts = integrator.get_active_alerts()
    assert isinstance(alerts, list)

def test_error_handling(integrator):
    try:
        integrator.analyze_location("Zurich", {})
        assert False, "Should raise an exception"
    except (ValueError, KeyError):
        assert True

def test_state_persistence(integrator, test_metrics):
    # Primera llamada y captura del estado inicial
    integrator.analyze_location("Zurich", test_metrics)
    initial_time = integrator.get_system_state().last_update
    
    # Esperamos un segundo para asegurar diferencia de tiempo
    time.sleep(1.0)
    
    # Actualizamos el estado
    test_metrics['sales_growth']['current'] = 1100  # Cambiamos un valor para forzar actualización
    integrator.analyze_location("Zurich", test_metrics)
    final_time = integrator.get_system_state().last_update
    
    # Comparamos los timestamps asegurando que hay diferencia
    assert final_time > initial_time, f"Final time {final_time} should be greater than initial time {initial_time}"