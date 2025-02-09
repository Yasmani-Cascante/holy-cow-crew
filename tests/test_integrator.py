import pytest
from datetime import datetime
from src.integrator import HolyCowIntegrator

@pytest.fixture
def integrator():
    return HolyCowIntegrator()

@pytest.fixture
def sample_metrics():
    """Datos de ejemplo para pruebas"""
    return {
        'sales_growth': {
            'current': -2,
            'previous': 2,
            'target': 5,
            'unit': '%'
        },
        'staff_efficiency': {
            'current': 65,
            'previous': 75,
            'target': 85,
            'unit': '%'
        },
        'inventory_turnover': {
            'current': 25,
            'previous': 20,
            'target': 15,
            'unit': 'days'
        }
    }

def test_integrator_initialization(integrator):
    """Prueba la inicialización correcta del integrador"""
    assert integrator is not None
    state = integrator.get_system_state()
    assert len(state.locations) == 3
    assert all(state.system_health.values())

def test_analyze_location(integrator, sample_metrics):
    """Prueba el análisis integrado de una ubicación"""
    result = integrator.analyze_location('Zurich', sample_metrics)
    
    # Verificar estructura básica
    assert result.location == 'Zurich'
    assert isinstance(result.timestamp, datetime)
    
    # Verificar componentes
    assert 'performance_metrics' in result.dict()
    assert 'market_insights' in result.dict()
    assert 'dashboard_data' in result.dict()

def test_system_health_monitoring(integrator):
    """Prueba el monitoreo de salud del sistema"""
    state = integrator.get_system_state()
    
    # Verificar estado inicial
    assert all(state.system_health.values())
    assert len(state.locations) == 3
    assert isinstance(state.last_update, datetime)

def test_error_handling(integrator):
    """Prueba el manejo de errores"""
    with pytest.raises(Exception):
        # Ubicación inválida debería lanzar una excepción
        integrator.analyze_location('InvalidLocation', {})