from crewai import Agent, Task, Crew, Process
from src.agents import (
    PerformanceAnalysisAgent,
    MarketingAgent,
    ResourceOptimizationAgent,
    ReportingAgent
)
from src.tools.data_loader import load_test_scenarios
from src.utils.logging_config import setup_logging
from src.utils.metrics import TestMetrics
from src.models.inventory_models import InventoryLevel, InventoryItem
from src.models.resource_models import ResourceOptimizationInput
from datetime import datetime
from textwrap import dedent
import logging

logger = setup_logging()
metrics = TestMetrics()

def run_tests():
    try:
        logger.info("Iniciando pruebas del sistema Holy Cow")
        locations = ["Zurich", "Geneva", "Basel"]
        results = {}
        
        for location in locations:
            logger.info(f"\nIniciando análisis para {location}...")
            location_results = test_holy_cow_system(location)
            results[location] = location_results
            logger.info(f"\nAnálisis completado para {location}")
            logger.info("="*50)
            
        return results
        
    except Exception as e:
        logger.error(f"Error en run_tests: {str(e)}")
        raise

def test_holy_cow_system(location: str = "Zurich"):
    try:
        metrics.start_test(location)
        logger.info(f"Iniciando pruebas para {location}")
        
        scenarios = load_test_scenarios()
        location_data = scenarios[location]
        sales_data = location_data['sales_data']
        
        agents = {
            "performance": PerformanceAnalysisAgent().get_agent(),
            "marketing": MarketingAgent().get_agent(),
            "resource": ResourceOptimizationAgent().get_agent(),
            "reporting": ReportingAgent().get_agent()
        }
        
        tasks = _create_tasks(location, location_data, agents)
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        results = crew.kickoff()
        metrics.end_test(location)
        logger.info(f"Pruebas completadas para {location}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error en test_holy_cow_system: {str(e)}")
        raise

def _create_tasks(location: str, location_data: dict, agents: dict) -> list[Task]:
    tasks = []
    
    # Task 1: Performance Analysis
    tasks.append(Task(
        description=dedent(f"""
        Analiza el rendimiento del restaurante en {location}:
        1. Revisa la precisión de las predicciones de ventas
        2. Identifica patrones en el rendimiento
        3. Analiza métricas clave
        4. Proporciona recomendaciones específicas basadas en los datos
        
        Datos de ventas:
        {str(location_data['sales_data'])}
        """),
        expected_output=dedent("""
        Un análisis detallado que incluya:
        1. Métricas de predicción (MAE, MAPE)
        2. Patrones identificados
        3. KPIs relevantes
        4. Recomendaciones basadas en datos
        """),
        agent=agents["performance"]
    ))
    
    # Task 2: Resource Optimization
    tasks.append(Task(
        description=dedent(f"""
        Optimiza los recursos del restaurante en {location}:
        1. Analiza los niveles actuales de personal
        2. Revisa el inventario y su utilización
        3. Identifica ineficiencias y cuellos de botella
        4. Proporciona un plan detallado de optimización
        
        Datos actuales:
        {str(location_data['sales_data'])}
        """),
        expected_output=dedent("""
        Un plan de optimización que incluya:
        1. Recomendaciones de personal por turno
        2. Plan de inventario optimizado
        3. Identificación de ineficiencias
        4. Medidas correctivas propuestas
        """),
        agent=agents["resource"]
    ))
    
    # Task 3: Market Strategy
    tasks.append(Task(
        description=dedent(f"""
        Desarrolla estrategia de marketing para {location}:
        1. Analiza el rendimiento actual
        2. Evalúa tendencias locales
        3. Analiza el perfil demográfico
        4. Proporciona recomendaciones
        
        Datos de mercado:
        {str(location_data.get('market_data', {}))}
        """),
        expected_output=dedent("""
        Una estrategia de marketing que incluya:
        1. Análisis del mercado objetivo
        2. Propuestas de campañas
        3. Plan de medios recomendado
        4. Métricas de éxito esperadas
        """),
        agent=agents["marketing"]
    ))
    
    return tasks

if __name__ == "__main__":
    run_tests()