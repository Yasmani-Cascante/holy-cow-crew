import os
import sys
from pathlib import Path
import traceback

def test_full_analysis():
    """Prueba completa del sistema de análisis"""
    try:
        print("=== Iniciando prueba completa del sistema ===\n")
        
        # 1. Verificar estructura de directorios
        required_dirs = ['data/sample', 'data/reports', 'src/agents', 'src/tools', 'src/models']
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                print(f"Creando directorio: {dir_path}")
                os.makedirs(dir_path, exist_ok=True)
        
        # 2. Verificar archivos necesarios
        required_files = [
            'data/sample/sales_history.csv',
            'data/sample/inventory.csv',
            'data/sample/staff_metrics.csv'
        ]
        for file_path in required_files:
            if not os.path.exists(file_path):
                print(f"ERROR: Archivo requerido no encontrado: {file_path}")
                return False
        
        # 3. Importar y ejecutar análisis
        from src.run_test_crew import run_restaurant_optimization
        print("\nEjecutando análisis completo...")
        results, report = run_restaurant_optimization()
        
        # 4. Verificar resultados
        for location in ['Zurich', 'Geneva', 'Basel']:
            if location not in results:
                print(f"ERROR: Resultados faltantes para {location}")
                return False
            
            location_data = results[location]
            if not location_data['success']:
                print(f"ERROR en {location}: {location_data.get('error', 'Error desconocido')}")
                return False
            
            # Verificar métricas básicas
            metrics = location_data.get('metrics', {})
            if not all(k in metrics for k in ['sales', 'staff', 'inventory']):
                print(f"ERROR: Métricas incompletas para {location}")
                return False
        
        # 5. Verificar reporte
        if not report or len(report) < 100:  # El reporte debería ser sustancial
            print("ERROR: Reporte generado está vacío o es muy corto")
            return False
        
        print("\n=== Prueba completada exitosamente ===")
        print("\nReporte generado:")
        print("-" * 50)
        print(report)
        return True
        
    except Exception as e:
        print(f"\nERROR durante la prueba: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\nIniciando pruebas del sistema...")
    success = test_full_analysis()
    print(f"\nResultado final: {'ÉXITO' if success else 'FALLO'}")
    sys.exit(0 if success else 1)