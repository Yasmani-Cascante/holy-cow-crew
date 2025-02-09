from src.agents.reporting_agent import ReportingAgent
from datetime import datetime

def simulate_restaurant_data():
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

def main():
    # Inicializar agente
    print("Inicializando Reporting Agent...")
    agent = ReportingAgent()
    
    # Simular datos
    print("\nGenerando datos de prueba...")
    test_data = simulate_restaurant_data()
    
    # Generar dashboard
    print("\nCreando dashboard para Zurich...")
    result = agent.create_dashboard('Zurich', test_data)
    
    # Mostrar resultados
    print("\n=== Dashboard Configuration ===")
    print(f"Title: {result['config'].title}")
    print(f"Widgets: {len(result['config'].widgets)}")
    
    print("\n=== KPIs ===")
    for kpi in result['kpis']:
        print(f"{kpi.name}:")
        print(f"  Value: {kpi.value}{kpi.unit}")
        print(f"  Target: {kpi.target}{kpi.unit}")
        print(f"  Trend: {kpi.trend:+.1f}{kpi.unit}")
    
    print("\n=== Active Alerts ===")
    for alert in result['alerts']:
        print(f"[{alert.level.upper()}] {alert.message}")

if __name__ == "__main__":
    main()