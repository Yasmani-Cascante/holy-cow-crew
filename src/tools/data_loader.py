#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def get_project_root() -> str:
    """Returns project root directory"""
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def load_test_scenarios() -> Dict[str, Any]:
    """
    Carga los escenarios de prueba desde el archivo JSON
    
    Returns:
        Dict con los datos de prueba
    """
    try:
        file_path = os.path.join(get_project_root(), 'data', 'sample', 'test_scenarios.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Archivo de escenarios no encontrado: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decodificando JSON: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error cargando escenarios de prueba: {str(e)}")
        raise

def load_inventory_data() -> Dict[str, Any]:
    """
    Carga datos de inventario desde CSV
    
    Returns:
        Dict con datos de inventario procesados
    """
    try:
        file_path = os.path.join(get_project_root(), 'data', 'sample', 'inventory.csv')
        import pandas as pd
        df = pd.read_csv(file_path)
        return df.to_dict('records')
    except Exception as e:
        logger.error(f"Error cargando datos de inventario: {str(e)}")
        raise

def load_sales_history() -> Dict[str, Any]:
    """
    Carga historial de ventas desde CSV
    
    Returns:
        Dict con historial de ventas procesado
    """
    try:
        file_path = os.path.join(get_project_root(), 'data', 'sample', 'sales_history.csv')
        import pandas as pd
        df = pd.read_csv(file_path)
        return df.to_dict('records')
    except Exception as e:
        logger.error(f"Error cargando historial de ventas: {str(e)}")
        raise