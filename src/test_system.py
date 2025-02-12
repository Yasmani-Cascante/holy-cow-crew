#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
from textwrap import dedent
import traceback
from typing import Dict, Any
import json
from pathlib import Path

logger = setup_logging()
metrics = TestMetrics()

def test_holy_cow_system(location: str = "Zurich") -> Dict[str, Any]:
    """Ejecuta una serie de tareas de prueba para el sistema Holy Cow"""
    
    try:
        metrics.start_test(location)
        logger.info(f"Iniciando pruebas para {location}")
        
        # Inicializar agentes
        agents = {
            "performance": PerformanceAnalysisAgent().get_agent(),
            "marketing": MarketingAgent().get_agent(),
            "resource": ResourceOptimizationAgent().get_agent(),
            "reporting": ReportingAgent().get_agent()
        }
        
        # Cargar datos de prueba para la ubicación
        test_data = load_test_scenarios()
        location_data = test_data[location]
        
        # Definir y ejecutar tareas
        tasks = _create_tasks(location, location_data, agents)
        
        # Crear y ejecutar crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Ejecutar y capturar resultados
        results = crew.kickoff()
        
        # Evaluar recomendaciones
        if isinstance(results, dict) and "recommendations" in results:
            metrics.evaluate_recommendations(location, results["recommendations"])
        
        # Registrar fin de prueba
        metrics.end_test(location)
        logger.info(f"Pruebas completadas para {location}")
        
        return results
        
    except Exception as e:
        error_msg = f"Error en test_holy_cow_system: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        metrics.record_error(location, type(e).__name__, str(e))
        raise

def _create_tasks(location: str, location_data: Dict[str, Any], agents: Dict[str, Agent]) -> list[Task]:
    """Crea las tareas para el crew"""
    
    tasks = []
    
    # Tarea 1: Análisis inicial de rendimiento
    performance_task = Task(
        description=dedent(f"""Analiza el rendimiento del restaurante en {location}:
        1. Revisa la precisión de las predicciones de ventas
        2. Identifica patrones en el rendimiento
        3. Analiza métricas clave
        4. Proporciona recomendaciones específicas basadas en los datos
        
        Datos de ventas:
        {str(location_data['sales_data'])}"""),
        expected_output=dedent("""Proporciona un análisis detallado que incluya:
        1. Métricas de precisión de predicciones (MAE, MAPE)
        2. Patrones identificados en ventas y rendimiento
        3. KPIs relevantes con sus valores actuales
        4. Lista priorizada de recomendaciones basadas en datos
        
        El formato debe ser estructurado y cuantitativo cuando sea posible."""),
        agent=agents["performance"]
    )
    tasks.append(performance_task)

    # Tarea 2: Optimización de recursos
    resource_task = Task(
        description=dedent(f"""Optimiza los recursos del restaurante en {location}:
        1. Analiza los niveles actuales de personal
        2. Revisa el inventario y su utilización
        3. Identifica ineficiencias y cuellos de botella
        4. Proporciona un plan detallado de optimización
        
        Datos actuales:
        {str(location_data['sales_data'])}"""),
        expected_output=dedent("""Entrega un plan de optimización que incluya:
        1. Análisis de personal actual vs. necesario por turno
        2. Métricas de utilización de inventario y recomendaciones
        3. Lista de ineficiencias identificadas con impacto estimado
        4. Plan de acción priorizado con costos y beneficios esperados
        
        Incluye datos cuantitativos para respaldar las recomendaciones."""),
        agent=agents["resource"],
        context=[performance_task]
    )
    tasks.append(resource_task)

    # Tarea 3: Estrategia de marketing
    marketing_task = Task(
        description=dedent(f"""Desarrolla una estrategia de marketing para {location}:
        1. Analiza los resultados de rendimiento
        2. Considera las recomendaciones de recursos
        3. Evalúa tendencias locales y eventos próximos
        4. Analiza el perfil demográfico de la zona
        
        Datos del mercado:
        {str(location_data['market_data'])}"""),
        expected_output=dedent("""Proporciona una estrategia de marketing que incluya:
        1. Análisis del mercado objetivo y competencia
        2. Propuestas de campañas específicas con ROI esperado
        3. Plan de medios y canales recomendados
        4. Presupuesto estimado y métricas de éxito
        
        La estrategia debe alinearse con los hallazgos previos."""),
        agent=agents["marketing"],
        context=[performance_task, resource_task]
    )
    tasks.append(marketing_task)

    # Tarea 4: Informe final y dashboard
    reporting_task = Task(
        description=dedent(f"""Genera un informe completo para {location}:
        1. Resume los hallazgos clave
        2. Presenta el plan de optimización
        3. Detalla la estrategia de marketing
        4. Visualiza KPIs y métricas clave
        5. Proporciona recomendaciones priorizadas
        
        Datos completos:
        {str(location_data)}"""),
        expected_output=dedent("""Entrega un informe ejecutivo estructurado que contenga:
        1. Resumen ejecutivo con hallazgos clave
        2. Dashboard con KPIs principales y tendencias
        3. Recomendaciones consolidadas y priorizadas
        4. Plan de implementación con timeline
        5. Métricas de seguimiento propuestas
        
        El informe debe ser claro, accionable y respaldado por datos."""),
        agent=agents["reporting"],
        context=[performance_task, resource_task, marketing_task]
    )
    tasks.append(reporting_task)
    
    return tasks

def run_tests():
    """Ejecuta pruebas del sistema para todas las ubicaciones"""
    try:
        # Lista de ubicaciones para probar
        locations = ["Zurich", "Geneva", "Basel"]
        results = {}
        
        for location in locations:
            logger.info(f"\nIniciando análisis para {location}...")
            
            # Ejecutar pruebas para la ubicación
            location_results = test_holy_cow_system(location)
            results[location] = location_results
            
            logger.info(f"\nAnálisis completado para {location}")
            logger.info("="*50)
        
        # Guardar resultados y métricas
        output_dir = Path("data/results")
        output_dir.mkdir(exist_ok=True)
        
        # Guardar métricas
        metrics_file = metrics.save_metrics(str(output_dir))
        logger.info(f"Métricas guardadas en: {metrics_file}")
        
        # Guardar resultados detallados
        results_file = output_dir / f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Resultados guardados en: {results_file}")
        
        return results

    except Exception as e:
        logger.error(f"Error en run_tests: {str(e)}\n{traceback.format_exc()}")
        raise

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        logger.critical(f"Error crítico en la ejecución: {str(e)}")
        raise