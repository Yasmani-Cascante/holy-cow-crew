from src.integrator import HolyCowIntegrator

def main():
    integrator = HolyCowIntegrator()
    
    # Datos de prueba
    test_metrics = {
        'inventory_turnover': {'current': 25, 'previous': 20, 'target': 15, 'unit': 'days'},
        'sales_growth': {'current': -2, 'previous': 2, 'target': 5, 'unit': '%'},
        'staff_efficiency': {'current': 65, 'previous': 75, 'target': 85, 'unit': '%'}
    }

    # Ejecutar análisis integrado
    result = integrator.analyze_location('Zurich', test_metrics)
    print(result.model_dump())

if __name__ == "__main__":
    main()