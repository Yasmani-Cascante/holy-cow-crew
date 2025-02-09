#!/usr/bin/env python3
"""
Script principal para ejecutar el análisis del sistema Holy Cow Crew.
Este script configura el entorno y ejecuta el análisis completo del restaurante.
"""

import os
import sys
from pathlib import Path
import logging
from datetime import datetime

# Configurar logging
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(
            log_dir / f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurar paths
PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))
os.environ['PYTHONPATH'] = str(PROJECT_ROOT)

def main():
    """Función principal que ejecuta el análisis"""
    logger.info("Iniciando análisis de Holy Cow Crew...")
    
    try:
        # Importar nuestros módulos
        from src.run_test_crew import run_restaurant_optimization
        
        # Ejecutar análisis
        results, report = run_restaurant_optimization()
        
        logger.info("Análisis completado con éxito!")
        
        # Mostrar reporte
        print("\nContenido del Reporte:")
        print(report)
        
        # Verificar resultados
        successful_locations = sum(
            1 for data in results.values() 
            if data.get('success', False)
        )
        total_locations = len(results)
        
        logger.info(
            f"Análisis completado para {successful_locations}/{total_locations} ubicaciones"
        )
        
        if successful_locations < total_locations:
            logger.warning("Algunas ubicaciones no pudieron ser analizadas")
            failed_locations = [
                location 
                for location, data in results.items() 
                if not data.get('success', False)
            ]
            logger.warning(f"Ubicaciones con error: {', '.join(failed_locations)}")
        
        return 0  # Éxito
        
    except ImportError as e:
        logger.error(f"Error importando módulos: {str(e)}")
        return 1
    except Exception as e:
        logger.error(f"Error durante el análisis: {str(e)}")
        import traceback
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    sys.exit(main())