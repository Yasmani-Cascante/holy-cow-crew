import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logging(log_dir: str = "data/results/logs") -> logging.Logger:
    """Configura el sistema de logging con rotación de archivos y formatos personalizados"""
    
    # Crear directorio de logs si no existe
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Configurar nombre de archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_path / f"holy_cow_test_{timestamp}.log"
    
    # Configurar logger
    logger = logging.getLogger("HolyCowTest")
    logger.setLevel(logging.DEBUG)
    
    # Handler para archivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formato detallado para archivo
    file_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(lineno)d | %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Formato simplificado para consola
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger