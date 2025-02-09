import pytest
from src.agents.resource_optimization_agent import ResourceOptimizationAgent
from src.tools.resource_tools import OptimizationResult

@pytest.fixture
def agent():
    return ResourceOptimizationAgent()

@pytest.fixture
def test_data():
    return {
        'predicted_sales': 5000,
        'current_staff': 10,
        'inventory_levels': {'item1': 3, 'item2': 8},
        'peak_hours': ['12:00', '13:00'],
        'day_of_week': 'monday'
    }

def test_optimize_resources(agent, test_data):
    result = agent.optimize_resources(test_data)
    assert isinstance(result, OptimizationResult)
    assert len(result.recommended_staff) > 0
    assert isinstance(result.efficiency_score, float)

def test_staff_recommendations(agent, test_data):
    result = agent.optimize_resources(test_data)
    staff_recs = result.recommended_staff
    assert len(staff_recs) == 3  # morning, afternoon, evening
    assert all(rec.staff_count > 0 for rec in staff_recs)

def test_inventory_optimization(agent, test_data):
    result = agent.optimize_resources(test_data)
    assert isinstance(result.inventory_orders, list)
    if test_data['inventory_levels']['item1'] < 5:
        assert any(order.item == 'item1' for order in result.inventory_orders)

def test_peak_hours_handling(agent, test_data):
    result = agent.optimize_resources(test_data)
    peak_shift = next(rec for rec in result.recommended_staff 
                     if any(hour in test_data['peak_hours'] 
                     for hour in ['12:00', '13:00', '14:00']))
    assert peak_shift.staff_count >= sum(rec.staff_count 
           for rec in result.recommended_staff if rec != peak_shift) / 2

def test_cost_savings(agent, test_data):
    result = agent.optimize_resources(test_data)
    assert result.cost_savings >= 0
    assert isinstance(result.cost_savings, float)

def test_edge_cases(agent):
    min_data = {
        'predicted_sales': 100,
        'current_staff': 1,
        'inventory_levels': {},
        'peak_hours': [],
        'day_of_week': 'monday'
    }
    result = agent.optimize_resources(min_data)
    assert isinstance(result, OptimizationResult)

def test_task_creation(agent):
    task = agent.create_optimization_task("Zurich")
    assert task.description
    assert task.expected_output
    assert task.agent

def test_inventory_priorities(agent, test_data):
    test_data['inventory_levels'] = {'critical_item': 1, 'normal_item': 6}
    result = agent.optimize_resources(test_data)
    critical_orders = [order for order in result.inventory_orders 
                      if order.priority == 'high']
    assert len(critical_orders) > 0