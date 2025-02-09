import os
import sys
from pathlib import Path

# Agregar directorio raíz del proyecto al PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Configuración de variables de entorno para pruebas
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'dummy-key-for-testing')
os.environ['ANTHROPIC_API_KEY'] = os.getenv('ANTHROPIC_API_KEY', 'dummy-key-for-testing')