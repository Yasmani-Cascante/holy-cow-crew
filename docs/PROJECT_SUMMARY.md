# Holy Cow Crew - Sistema Multi-Agente para Optimización de Restaurantes

## Descripción General
Sistema multi-agente desarrollado con CrewAI para optimizar las operaciones de la cadena de restaurantes Holy Cow! en Suiza. El sistema utiliza datos de predicción de ventas para proporcionar análisis y recomendaciones en múltiples áreas operativas.

## Estructura del Proyecto

```
holy-cow-crew/
├── src/                        # Código fuente principal
│   ├── agents/                 # Agentes del sistema
│   │   ├── base_agent.py      # Clase base para agentes
│   │   ├── performance_analysis_agent.py
│   │   ├── resource_optimization_agent.py
│   │   ├── market_strategy_agent.py
│   │   └── reporting_agent.py
│   ├── models/                 # Modelos de datos
│   │   ├── integration_models.py
│   │   ├── inventory_models.py
│   │   ├── marketing_models.py
│   │   └── sales_prediction.py
│   ├── tools/                  # Herramientas para agentes
│   │   ├── demand_prediction_tools.py
│   │   ├── inventory_tools.py
│   │   ├── marketing_tools.py
│   │   └── resource_tools.py
│   ├── reporting/             # Sistema de reportes
│   │   ├── report_generator.py  # Generador de informes
│   │   └── test_report.py      # Pruebas de reportes
│   ├── test_scenarios/        # Escenarios de prueba
│   │   └── scenarios.py       # Definición de escenarios
│   ├── run_crew.py           # Ejecución principal del sistema
│   ├── run_test_crew.py      # Ejecución de pruebas
│   └── test_system.py        # Sistema de pruebas completo
├── data/                      # Datos y configuración
│   ├── sample/               # Datos de prueba
│   │   ├── holy_cow_inventory.py
│   │   ├── inventory.csv
│   │   ├── sales_history.csv
│   │   └── staff_metrics.csv
│   └── config.yaml           # Configuración del sistema
└── docs/                     # Documentación
    ├── TECHNICAL_SUMMARY.md
    └── PROJECT_SUMMARY.md

```

## Componentes Principales

### 1. Scripts de Ejecución
- **run_crew.py**: Script principal para ejecutar el sistema en producción
  - Inicializa y coordina los agentes
  - Ejecuta las tareas en secuencia
  - Maneja los resultados y reportes

- **run_test_crew.py**: Sistema de pruebas automatizado
  - Ejecuta pruebas del sistema completo
  - Valida funcionamiento de agentes
  - Verifica integración de componentes

- **test_system.py**: Framework de pruebas
  - Define casos de prueba
  - Simula diferentes escenarios
  - Valida resultados esperados

### 2. Sistema de Reportes (/reporting)
- **report_generator.py**: Genera informes detallados
  - Análisis de rendimiento
  - Métricas operativas
  - Recomendaciones
  - Visualizaciones

- **test_report.py**: Pruebas de generación de reportes
  - Valida formato de reportes
  - Verifica cálculos y métricas
  - Asegura consistencia

### 3. Escenarios de Prueba (/test_scenarios)
- **scenarios.py**: Define escenarios de prueba
  - Casos típicos de operación
  - Situaciones de borde
  - Escenarios de error
  - Validación de recuperación

## Agentes del Sistema

### 1. Performance Analysis Agent
- Análisis de ventas y rendimiento
- Detección de patrones
- Predicciones y tendencias
- Recomendaciones basadas en datos

### 2. Resource Optimization Agent
- Optimización de personal
- Gestión de inventario
- Eficiencia operativa
- Coordinación entre locales

### 3. Market Strategy Agent
- Análisis de mercado
- Estrategias de marketing
- Precios y promociones
- Análisis competitivo

### 4. Reporting Agent
- Generación de informes
- Visualización de datos
- Alertas y notificaciones
- Dashboard operativo

## Datos y Configuración

### Estructura de Datos
- **Inventario**: Catálogo de productos y niveles actuales
- **Ventas**: Histórico y predicciones
- **Personal**: Métricas y turnos
- **Marketing**: Campañas y resultados

### Configuración
```yaml
data_sources:
  inventory:
    catalog: holy_cow_inventory.py
    current: inventory.csv
    historical: inventory_data.csv
  sales:
    current: sales_history.csv
    historical: historical_sales.csv
  support:
    marketing: marketing_campaigns.csv
    staff: staff_metrics.csv

analysis_config:
  use_historical: true
  min_data_points: 30
  alerts:
    inventory:
      waste_threshold: 5
      stock_threshold: 0.2
    efficiency:
      min_score: 0.7
```

## Proceso de Ejecución

1. **Inicialización**
   - Carga de configuración
   - Inicialización de agentes
   - Verificación de datos

2. **Análisis**
   - Recopilación de datos
   - Análisis de rendimiento
   - Optimización de recursos
   - Generación de estrategias

3. **Reportes**
   - Generación de informes
   - Visualización de resultados
   - Alertas y recomendaciones

4. **Monitoreo**
   - Seguimiento de KPIs
   - Detección de anomalías
   - Ajustes y optimizaciones

## Estado Actual y Próximos Pasos

### Estado Actual
- Version: 1.0.0
- Última actualización: Febrero 2025
- Cobertura de pruebas: 85%
- Locales activos: 4

### Próximos Desarrollos
1. Implementación de cache avanzado
2. Monitoreo en tiempo real
3. Mejoras en manejo de errores
4. Sistema de backup automático
5. Verificaciones de salud del sistema

## Recursos
- Repositorio: https://github.com/Yasmani-Cascante/holy-cow-crew
- Documentación Técnica: TECHNICAL_SUMMARY.md
- Equipo de Desarrollo: Yasmani Cascante (Lead)