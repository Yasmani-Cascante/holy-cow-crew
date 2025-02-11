#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from crewai import Agent, Task, Crew, Process
from .agents import (
    PerformanceAnalysisAgent,
    MarketingAgent,
    ResourceOptimizationAgent,
    ReportingAgent
)
from .tools.data_loader import load_test_scenarios
from textwrap import dedent

logger = logging.getLogger(__name__)

def test_holy_cow_system(location: str = "Zurich"):
    """Ejecuta una serie de tareas de prueba para el sistema Holy Cow"""
    
    try:
        # Inicializar agentes
        performance_agent = PerformanceAnalysisAgent().get_agent()
        marketing_agent = MarketingAgent().get_agent()
        resource_agent = ResourceOptimizationAgent().get_agent()
        reporting_agent = ReportingAgent().get_agent()
        
        # Cargar datos de prueba para la ubicación
        test_data = load_test_scenarios()
        location_data = test_data[location]
        
        # Tarea 1: Análisis inicial de rendimiento
        performance_task = Task(
            description=dedent(f"""Analiza el rendimiento del restaurante en {location}:
            1. Revisa la precisión de las predicciones de ventas
            2. Identifica patrones en el rendimiento
            3. Analiza métricas clave
            4. Proporciona recomendaciones específicas basadas en los datos
            
            Datos de ventas:
            {str(location_data['sales_data'])}"""),
            agent=performance_agent
        )

        # Tarea 2: Optimización de recursos
        resource_task = Task(
            description=dedent(f"""Optimiza los recursos del restaurante en {location} basándote en el análisis de rendimiento:
            1. Analiza los niveles actuales de personal
            2. Revisa el inventario y su utilización
            3. Identifica ineficiencias y cuellos de botella
            4. Proporciona un plan detallado de optimización
            
            Datos actuales:
            {str(location_data['sales_data'])}"""),
            agent=resource_agent,
            context=[performance_task]
        )

        # Tarea 3: Estrategia de marketing
        marketing_task = Task(
            description=dedent(f"""Desarrolla una estrategia de marketing para {location} considerando:
            1. Los resultados del análisis de rendimiento
            2. Las recomendaciones de optimización de recursos
            3. Las tendencias locales y eventos próximos
            4. El perfil demográfico de la zona
            
            Datos del mercado:
            {str(location_data['market_data'])}"""),
            agent=marketing_agent,
            context=[performance_task, resource_task]
        )

        # Tarea 4: Informe final y dashboard
        reporting_task = Task(
            description=dedent(f"""Genera un informe completo y dashboard para {location} que incluya:
            1. Resumen ejecutivo del rendimiento
            2. Plan de optimización de recursos
            3. Estrategia de marketing propuesta
            4. KPIs y métricas clave
            5. Visualizaciones relevantes
            
            Datos completos:
            {str(location_data)}"""),
            agent=reporting_agent,
            context=[performance_task, resource_task, marketing_task]
        )

        # Crear el crew con todos los agentes y tareas
        crew = Crew(
            agents=[
                performance_agent,
                resource_agent,
                marketing_agent,
                reporting_agent
            ],
            tasks=[
                performance_task,
                resource_task,
                marketing_task,
                reporting_task
            ],
            process=Process.sequential,
            verbose=True
        )

        return crew

    except Exception as e:
        logger.error(f"Error en test_holy_cow_system: {str(e)}")
        raise

def run_tests():
    """Ejecuta pruebas del sistema para todas las ubicaciones"""
    try:
        # Lista de ubicaciones para probar
        locations = ["Zurich", "Geneva", "Basel"]
        results = {}

        for location in locations:
            logger.info(f"\nIniciando análisis para {location}...")
            crew = test_holy_cow_system(location)
            results[location] = crew.kickoff()
            logger.info(f"\nAnálisis completado para {location}")
            logger.info("="*50)

        # Imprimir resultados
        for location, result in results.items():
            logger.info(f"\nResultados para {location}:")
            logger.info("-"*30)
            logger.info(result)
            logger.info("="*50)

        return results

    except Exception as e:
        logger.error(f"Error en run_tests: {str(e)}")
        raise

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    run_tests()