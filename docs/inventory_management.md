# Sistema de Gestión de Inventario

## Descripción General
El sistema de gestión de inventario proporciona análisis avanzado y recomendaciones para la optimización del inventario en los restaurantes Holy Cow. Utiliza análisis histórico, predicciones de ventas y factores estacionales para generar recomendaciones precisas.

## Características Principales

### 1. Categorización de Items
- Perecederos
- Congelados
- Productos secos
- Bebidas
- Suministros

### 2. Control de Almacenamiento
- Temperatura ambiente
- Refrigerado
- Congelado

### 3. Análisis Avanzado
- Uso diario promedio
- Tendencias de consumo
- Factores estacionales
- Predicción de necesidades

### 4. Recomendaciones de Pedidos
- Priorización inteligente
- Cantidades óptimas
- Timing sugerido
- Justificación detallada

## Ejemplo de Uso

```python
from src.agents.resource_optimization_agent import ResourceOptimizationAgent
from src.models.inventory_models import (
    InventoryItem,
    InventoryLevel,
    ItemCategory,
    StorageCondition
)
from datetime import datetime

# Crear agente
agent = ResourceOptimizationAgent()

# Preparar datos
data = {
    "location": "Zurich-Central",
    "predicted_sales": 5000,
    "inventory_items": {
        "BUN001": InventoryItem(
            id="BUN001",
            name="Hamburger Buns",
            category=ItemCategory.PERISHABLE,
            storage=StorageCondition.ROOM_TEMP,
            unit="pack",
            min_level=50,
            max_level=200,
            reorder_point=75,
            lead_time_days=2,
            shelf_life_days=5,
            cost_per_unit=3.50,
            supplier_id="SUP001"
        )
    },
    "inventory_levels": {
        "BUN001": InventoryLevel(
            item_id="BUN001",
            current_quantity=60,
            reserved_quantity=10,
            available_quantity=50,
            last_updated=datetime.now()
        )
    }
}

# Obtener optimización
result = agent.optimize_resources(data)

# Procesar resultados
inventory_recs = result['inventory_recommendations']
for item_id, rec in inventory_recs.items():
    print(f"\nRecomendación para {rec.name}:")
    print(f"Cantidad a pedir: {rec.quantity} {data['inventory_items'][item_id].unit}")
    print(f"Prioridad: {rec.priority}")
    print(f"Razón: {rec.reason}")
    print(f"Fecha sugerida de pedido: {rec.suggested_order_date}")
    print(f"Costo estimado: CHF {rec.estimated_cost:.2f}")
```

## Configuración

### Variables de Entorno
```env
SAFETY_STOCK_DAYS=3
SEASONAL_ADJUSTMENT_ENABLED=true
```

### Factores Estacionales por Defecto
```python
seasonal_factors = {
    'summer': 1.2,  # 20% más en verano
    'winter': 0.9,  # 10% menos en invierno
    'spring': 1.0,  # Normal
    'fall': 1.0     # Normal
}
```

## Integración con Otros Sistemas

### 1. Sistema de Predicción de Ventas
El sistema utiliza predicciones de ventas para ajustar las recomendaciones de inventario.

### 2. Sistema de Personal
Se integra con la optimización de personal para asegurar niveles adecuados de inventario según la capacidad operativa.

### 3. Análisis de Rendimiento
Proporciona datos para el análisis de rendimiento general del restaurante.

## Mejores Prácticas

1. **Configuración de Niveles**
   - Establecer niveles mínimos considerando lead times
   - Ajustar máximos según capacidad de almacenamiento
   - Revisar puntos de reorden periódicamente

2. **Gestión de Perecederos**
   - Monitorear fechas de caducidad
   - Rotar stock adecuadamente
   - Ajustar pedidos según vida útil

3. **Análisis Regular**
   - Revisar tendencias semanalmente
   - Ajustar factores estacionales
   - Validar predicciones vs realidad

## Métricas Clave

1. **Eficiencia de Inventario**
   - Rotación de inventario
   - Días de inventario
   - Pérdidas por caducidad

2. **Costos**
   - Costo de mantener inventario
   - Costo de pedidos
   - Pérdidas por faltantes

3. **Servicio**
   - Disponibilidad de productos
   - Tiempo de respuesta a faltantes
   - Satisfacción del cliente

## Mantenimiento

1. **Actualización de Datos**
   - Actualizar costos regularmente
   - Revisar lead times
   - Actualizar información de proveedores

2. **Calibración del Sistema**
   - Ajustar factores estacionales
   - Revisar niveles de stock de seguridad
   - Actualizar parámetros de priorización