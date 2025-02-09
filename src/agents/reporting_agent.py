"""
Agente especializado en la creación de reportes y visualizaciones.
"""

from crewai import Agent
from typing import Dict, List, Any, Optional
from ..tools.reporting_tools import ReportingTools
from datetime import datetime
import pandas as pd
import numpy as np

class ReportingAgent:
    """Agente especializado en la creación de reportes y visualizaciones"""
    
    def __init__(self):
        self.tools = ReportingTools()
        self.agent = self.create_agent()
    
    def create_agent(self) -> Agent:
        """Crea el agente de CrewAI"""
        return Agent(
            role='Reporting and Visualization Specialist',
            goal='Create comprehensive and insightful reports with interactive visualizations',
            backstory="""Expert in data visualization and reporting, specializing in 
            restaurant analytics. Skilled in creating interactive dashboards, generating 
            detailed reports, and providing actionable insights through data visualization.""",
            tools=self.tools.get_tools(),
            verbose=True
        )

    def create_report(self, location: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Genera un reporte completo con visualizaciones"""
        try:
            # Generar el reporte base usando las herramientas
            report_data = self.tools.create_report(location, data)
            
            if not report_data['success']:
                print(f"Error generando reporte para {location}: {report_data.get('error', 'Error desconocido')}")
                return {
                    'success': False,
                    'error': report_data.get('error', 'Error desconocido')
                }
            
            # Extraer las visualizaciones y otros componentes
            visualizations = report_data.get('visualizations', {})
            kpis = report_data.get('kpis', [])
            alerts = report_data.get('alerts', [])
            recommendations = report_data.get('recommendations', [])
            
            # Preparar datos específicos de ventas
            if 'sales' in data:
                sales = data['sales']
                sales_metrics = {
                    'total': float(sales.get('total', 0)),
                    'transactions': int(sales.get('transactions', 0)),
                    'peak_hours': sales.get('peak_hours', []),
                }
                
                # Asegurar que tenemos la visualización de ventas por hora
                if 'sales_hourly' not in visualizations:
                    sales_data = [
                        {'hour': hour, 'sales': sales_metrics['total'] * (0.12 if hour in sales_metrics['peak_hours'] else 0.04)}
                        for hour in range(8, 22)
                    ]
                    visualizations['sales_hourly'] = self.tools._create_line_chart(sales_data, 'Ventas por Hora')
            
            # Preparar datos específicos de personal
            if 'staff' in data:
                staff = data['staff']
                staff_metrics = {
                    'total_count': int(staff.get('total_count', 0)),
                    'efficiency': float(staff.get('efficiency', 0)),
                    'satisfaction': float(staff.get('satisfaction', 0)),
                    'overtime_total': float(staff.get('overtime_total', 0))
                }
                
                # Asegurar que tenemos la visualización de eficiencia por turno
                if 'staff_efficiency' not in visualizations:
                    shifts = staff.get('shifts', [])
                    if not shifts:
                        # Crear distribución por defecto
                        total_staff = staff_metrics['total_count']
                        base_efficiency = staff_metrics['efficiency']
                        shifts = [
                            {'shift': 'Mañana', 'staff_count': total_staff * 0.4, 'efficiency_score': base_efficiency},
                            {'shift': 'Tarde', 'staff_count': total_staff * 0.35, 'efficiency_score': base_efficiency},
                            {'shift': 'Noche', 'staff_count': total_staff * 0.25, 'efficiency_score': base_efficiency}
                        ]
                    visualizations['staff_efficiency'] = self.tools._create_bar_chart(
                        [{'label': s['shift'], 'value': s['efficiency_score'] * 100} for s in shifts],
                        'Eficiencia por Turno'
                    )
            
            # Preparar datos específicos de inventario
            if 'inventory' in data:
                inventory = data['inventory']
                
                # Asegurar que tenemos la visualización de niveles de inventario
                if 'inventory_levels' not in visualizations:
                    inventory_data = [
                        {
                            'label': item_name,
                            'value': item_info['quantity'],
                            'minimum': item_info['minimum_stock']
                        }
                        for item_name, item_info in inventory.items()
                        if isinstance(item_info, dict)
                    ]
                    visualizations['inventory_levels'] = self.tools._create_bar_chart(
                        inventory_data,
                        'Niveles de Inventario'
                    )
            
            return {
                'success': True,
                'report': {
                    'title': f"Reporte de Rendimiento - {location}",
                    'timestamp': datetime.now().isoformat(),
                    'location': location,
                    'kpis': kpis,
                    'alerts': alerts,
                    'recommendations': recommendations
                },
                'visualizations': visualizations
            }
            
        except Exception as e:
            print(f"Error generando reporte para {location}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_agent(self) -> Agent:
        """Retorna la instancia del agente"""
        return self.agent