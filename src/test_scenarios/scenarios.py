from typing import Dict, Any, List
from pydantic import BaseModel

class TestScenario(BaseModel):
    """Modelo para escenarios de prueba"""
    name: str
    description: str
    sales_multiplier: float = 1.0
    staff_modifier: float = 1.0
    inventory_modifier: float = 1.0
    expected_alerts: List[str] = []
    expected_kpis: Dict[str, float] = {}

# Definir escenarios predeterminados
DEFAULT_SCENARIOS = {
    'normal_operation': TestScenario(
        name='normal_operation',
        description='Normal operating conditions',
        sales_multiplier=1.0,
        staff_modifier=1.0,
        inventory_modifier=1.0,
        expected_alerts=[],
        expected_kpis={
            'efficiency': 85.0,
            'inventory_turnover': 7.0
        }
    ),
    'high_demand': TestScenario(
        name='high_demand',
        description='High demand scenario with increased sales',
        sales_multiplier=1.5,
        staff_modifier=1.0,
        inventory_modifier=0.8,
        expected_alerts=[
            'Staff levels may be insufficient for demand',
            'Low inventory alert'
        ],
        expected_kpis={
            'efficiency': 75.0,
            'inventory_turnover': 4.0
        }
    ),
    'low_demand': TestScenario(
        name='low_demand',
        description='Low demand scenario with reduced sales',
        sales_multiplier=0.7,
        staff_modifier=1.0,
        inventory_modifier=1.2,
        expected_alerts=[
            'Staff levels may be excessive for current demand',
            'High inventory levels detected'
        ],
        expected_kpis={
            'efficiency': 65.0,
            'inventory_turnover': 10.0
        }
    ),
    'staff_shortage': TestScenario(
        name='staff_shortage',
        description='Operating with reduced staff',
        sales_multiplier=1.0,
        staff_modifier=0.7,
        inventory_modifier=1.0,
        expected_alerts=[
            'Critical staff shortage detected',
            'Employee overtime alert'
        ],
        expected_kpis={
            'efficiency': 90.0,
            'inventory_turnover': 7.0
        }
    ),
    'peak_season': TestScenario(
        name='peak_season',
        description='Peak season operations',
        sales_multiplier=2.0,
        staff_modifier=1.5,
        inventory_modifier=1.5,
        expected_alerts=[
            'Near maximum capacity',
            'High staff utilization'
        ],
        expected_kpis={
            'efficiency': 95.0,
            'inventory_turnover': 3.0
        }
    )
}

def modify_test_data(data: Dict[str, Any], scenario: TestScenario) -> Dict[str, Any]:
    """Modifica los datos de prueba según el escenario"""
    modified_data = data.copy()
    
    # Modificar ventas
    if 'sales_growth' in modified_data:
        for key in ['current', 'previous']:
            modified_data['sales_growth'][key] *= scenario.sales_multiplier
    
    # Modificar personal
    if 'staff_count' in modified_data:
        modified_data['staff_count'] = int(modified_data['staff_count'] * scenario.staff_modifier)
    
    # Modificar inventario
    if 'inventory' in modified_data:
        modified_data['inventory'] = {
            item: quantity * scenario.inventory_modifier
            for item, quantity in modified_data['inventory'].items()
        }
    
    return modified_data