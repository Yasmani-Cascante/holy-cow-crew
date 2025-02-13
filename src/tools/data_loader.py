import os
import json
import logging
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime
from ..models.inventory_models import InventoryLevel, InventoryItem

logger = logging.getLogger(__name__)

def get_project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def load_test_scenarios() -> Dict[str, Any]:
    """Carga escenarios de prueba y convierte a modelos Pydantic"""
    try:
        file_path = os.path.join(get_project_root(), 'data', 'sample', 'test_scenarios.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            scenarios = json.load(f)
            
        # Convertir a modelos Pydantic
        for location in scenarios:
            if 'sales_data' in scenarios[location]:
                sales_data = scenarios[location]['sales_data']
                
                # Convertir inventory_levels a InventoryLevel
                if 'inventory_levels' in sales_data:
                    inventory_levels = {}
                    for item_id, level in sales_data['inventory_levels'].items():
                        inventory_levels[item_id] = InventoryLevel(
                            item_id=item_id,
                            current_quantity=float(level),
                            available_quantity=float(level),
                            last_updated=datetime.now()
                        )
                    sales_data['inventory_levels'] = inventory_levels
                
                # Convertir items a InventoryItem
                if 'items' in sales_data:
                    items = {}
                    for item_id, item_data in sales_data['items'].items():
                        items[item_id] = InventoryItem(**item_data)
                    sales_data['items'] = items
            
        return scenarios
            
    except Exception as e:
        logger.error(f"Error cargando escenarios: {str(e)}")
        raise

def load_sales_history() -> pd.DataFrame:
    """Carga historial de ventas"""
    try:
        file_path = os.path.join(get_project_root(), 'data', 'sample', 'sales_history.csv')
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except Exception as e:
        logger.error(f"Error cargando historial: {str(e)}")
        raise

def get_historical_data(
    location: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> pd.DataFrame:
    """Obtiene datos históricos filtrados"""
    df = load_sales_history()
    
    # Filtrar por ubicación
    df = df[df['location'] == location]
    
    # Filtrar por fechas si se especifican
    if start_date:
        df = df[df['date'] >= start_date]
    if end_date:
        df = df[df['date'] <= end_date]
        
    return df