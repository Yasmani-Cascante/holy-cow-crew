from crewai import Agent
from typing import Dict, List, Any
from ..tools.prediction_tools import PredictionTools
import numpy as np
from datetime import datetime

class PerformanceAnalysisAgent:
    """Agente responsable del análisis de rendimiento y predicciones"""
    
    def __init__(self):
        self.tools = PredictionTools()
        self.agent = self.create_agent()
        
    def create_agent(self) -> Agent:
        """Crea el agente de CrewAI"""
        return Agent(
            role='Performance Analysis Specialist',
            goal='Analyze sales prediction accuracy and provide actionable insights',
            backstory="""Expert in analyzing sales predictions and performance metrics 
            for the restaurant industry. Specializes in identifying patterns, anomalies, 
            and areas for improvement in prediction models. Has extensive experience in 
            the Swiss restaurant market.""",
            verbose=True
        )

    def process_sales_data(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Procesa y analiza datos de ventas"""
        analysis_results = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {},
            'insights': [],
            'recommendations': []
        }

        try:
            # Análisis de Ventas
            if 'sales' in metrics and isinstance(metrics['sales'], dict):
                sales = metrics['sales']
                total_sales = float(sales['total'])
                transactions = int(sales['transactions'])
                
                analysis_results['metrics']['sales'] = {
                    'total': total_sales,
                    'daily_average': total_sales / 30,  # Asumiendo mes de 30 días
                    'transactions': transactions,
                    'average_ticket': total_sales / transactions if transactions > 0 else 0
                }

                # Insights de ventas
                if total_sales > 50000:
                    analysis_results['insights'].append("Alto volumen de ventas - revisar capacidad operativa")
                elif total_sales < 20000:
                    analysis_results['insights'].append("Volumen de ventas bajo - considerar acciones promocionales")

            # Análisis de Personal
            if 'staff' in metrics and isinstance(metrics['staff'], dict):
                staff = metrics['staff']
                staff_count = int(staff['total_count'])
                
                analysis_results['metrics']['staff'] = {
                    'count': staff_count,
                    'efficiency': float(staff.get('efficiency', 0)),
                    'satisfaction': float(staff.get('satisfaction', 0)),
                    'overtime_hours': float(staff.get('overtime_total', 0))
                }

                # Análisis de productividad
                if 'sales' in metrics and isinstance(metrics['sales'], dict):
                    sales = metrics['sales']
                    total_sales = float(sales['total'])
                    sales_per_staff = total_sales / staff_count if staff_count > 0 else 0
                    
                    analysis_results['metrics']['productivity'] = {
                        'sales_per_staff': sales_per_staff,
                        'transactions_per_staff': transactions / staff_count if staff_count > 0 else 0
                    }

                    # Insights de productividad
                    if sales_per_staff < 1000:
                        analysis_results['insights'].append("Baja productividad por empleado - revisar asignación de turnos")
                    elif sales_per_staff > 3000:
                        analysis_results['insights'].append("Alta productividad - posible sobrecarga de personal")

            # Análisis de Inventario
            if 'inventory' in metrics and isinstance(metrics['inventory'], dict):
                inventory = metrics['inventory']
                total_items = len(inventory)
                items_below_min = 0
                
                for item_data in inventory.values():
                    if isinstance(item_data, dict):
                        quantity = float(item_data.get('quantity', 0))
                        min_stock = float(item_data.get('minimum_stock', 0))
                        if quantity <= min_stock:
                            items_below_min += 1
                
                analysis_results['metrics']['inventory'] = {
                    'total_items': total_items,
                    'items_below_minimum': items_below_min,
                    'health_score': (total_items - items_below_min) / total_items if total_items > 0 else 0
                }

                # Insights de inventario
                if items_below_min > 0:
                    analysis_results['insights'].append(
                        f"{items_below_min} items bajo mínimo - programar reposición"
                    )

            # Generar recomendaciones
            analysis_results['recommendations'] = self._generate_recommendations(analysis_results)

        except Exception as e:
            print(f"Error en el análisis de datos: {str(e)}")
            analysis_results['error'] = str(e)
            analysis_results['insights'].append("Error en el análisis - revisar datos de entrada")

        return analysis_results

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []

        if 'metrics' in analysis:
            metrics = analysis['metrics']
            
            # Recomendaciones de ventas
            if 'sales' in metrics:
                sales = metrics['sales']
                if sales.get('average_ticket', 0) < 50:
                    recommendations.append(
                        "Implementar estrategias de upselling para aumentar ticket promedio"
                    )

            # Recomendaciones de personal
            if 'staff' in metrics:
                staff = metrics['staff']
                if staff.get('efficiency', 0) < 0.8:
                    recommendations.append(
                        "Programar capacitación para mejorar eficiencia del personal"
                    )
                if staff.get('overtime_hours', 0) > 20:
                    recommendations.append(
                        "Revisar planificación de turnos para reducir horas extra"
                    )

            # Recomendaciones de inventario
            if 'inventory' in metrics:
                inventory = metrics['inventory']
                if inventory.get('health_score', 1) < 0.8:
                    recommendations.append(
                        "Optimizar gestión de inventario - revisar niveles mínimos"
                    )

        return recommendations

    def get_agent(self) -> Agent:
        """Retorna la instancia del agente"""
        return self.agent