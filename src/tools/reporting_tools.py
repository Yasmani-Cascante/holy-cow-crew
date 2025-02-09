"""
Herramientas para generación de reportes y visualizaciones.
"""

from langchain.tools import StructuredTool
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from ..models.reporting_models import KPIMetric, Alert

class ReportingTools:
    """Herramientas para generación de reportes y visualizaciones"""
    
    def __init__(self):
        self.kpi_thresholds = {
            'sales_total': {'warning': 20000, 'critical': 10000, 'target': 50000},
            'sales_growth': {'warning': 0, 'critical': -5, 'target': 10},
            'customer_satisfaction': {'warning': 85, 'critical': 75, 'target': 90},
            'inventory_turnover': {'warning': 14, 'critical': 21, 'target': 7},
            'staff_efficiency': {'warning': 80, 'critical': 70, 'target': 90}
        }

    def create_report(self, location: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea un reporte completo con visualizaciones"""
        try:
            # Calcular KPIs y generar alertas
            kpis = self.calculate_kpis(data)
            alerts = self.generate_alerts(kpis)
            
            # Generar visualizaciones
            visualizations = {
                'sales_hourly': self._create_line_chart(
                    self._prepare_sales_data(data.get('sales', {})),
                    'Ventas por Hora'
                ),
                'staff_efficiency': self._create_bar_chart(
                    self._prepare_staff_data(data.get('staff', {})),
                    'Eficiencia por Turno'
                ),
                'inventory_levels': self._create_bar_chart(
                    self._prepare_inventory_data(data.get('inventory', {})),
                    'Niveles de Inventario'
                )
            }
            
            # Generar recomendaciones
            recommendations = self.generate_recommendations(data, kpis, alerts)
            
            return {
                'success': True,
                'visualizations': visualizations,
                'kpis': [kpi.dict() for kpi in kpis],
                'alerts': [alert.dict() for alert in alerts],
                'recommendations': recommendations
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _create_line_chart(self, data: List[Dict[str, Any]], title: str) -> str:
        """Crea un gráfico de línea en ASCII art"""
        if not data:
            return "No hay datos disponibles"
            
        # Extraer valores
        labels = [item['label'] for item in data]
        values = [item['value'] for item in data]
        
        # Calcular dimensiones
        max_val = max(values) if values else 0
        min_val = min(values) if values else 0
        height = 10
        width = len(values)
        
        # Normalizar valores
        normalized = []
        if max_val != min_val:
            normalized = [(v - min_val) * (height - 1) / (max_val - min_val) for v in values]
        else:
            normalized = [0] * len(values)
        
        # Construir gráfico
        chart = [
            title,
            '-' * (width + 2)
        ]
        
        # Crear líneas
        for h in range(height - 1, -1, -1):
            line = ['|']
            for n in normalized:
                if n >= h:
                    line.append('*')
                else:
                    line.append(' ')
            line.append('|')
            chart.append(''.join(line))
        
        # Agregar eje X y leyenda
        chart.extend([
            '-' * (width + 2),
            f"Min: {min_val:,.0f}  Max: {max_val:,.0f}",
            ' '.join(str(label).rjust(2) for label in labels[:width])
        ])
        
        return '\n'.join(chart)

    def _create_bar_chart(self, data: List[Dict[str, Any]], title: str) -> str:
        """Crea un gráfico de barras en ASCII art"""
        if not data:
            return "No hay datos disponibles"
            
        # Extraer datos
        labels = [item['label'] for item in data]
        values = [item['value'] for item in data]
        
        # Calcular dimensiones
        max_val = max(values) if values else 0
        max_label_len = max(len(str(label)) for label in labels)
        bar_width = 30
        
        # Construir gráfico
        chart = [
            title,
            '=' * (max_label_len + bar_width + 15)
        ]
        
        # Crear barras
        for label, value in zip(labels, values):
            # Calcular longitud de la barra
            bar_length = int((value / max_val * bar_width) if max_val > 0 else 0)
            
            # Formatear valor
            value_str = f"{value:,.1f}"
            
            # Crear línea
            line = f"{str(label).ljust(max_label_len)} |{'█' * bar_length}{'░' * (bar_width - bar_length)}| {value_str}"
            chart.append(line)
        
        chart.append('=' * (max_label_len + bar_width + 15))
        return '\n'.join(chart)

    def _prepare_sales_data(self, sales_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepara datos de ventas para visualización"""
        if not isinstance(sales_data, dict):
            return []
            
        total_sales = float(sales_data.get('total', 0))
        peak_hours = sales_data.get('peak_hours', [12, 13, 19, 20])
        
        data = []
        for hour in range(8, 22):  # 8 AM a 10 PM
            is_peak = hour in peak_hours
            sales = total_sales * (0.12 if is_peak else 0.04)
            
            data.append({
                'label': f"{hour:02d}",
                'value': sales,
                'type': 'peak' if is_peak else 'normal'
            })
        
        return data

    def _prepare_staff_data(self, staff_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepara datos de personal para visualización"""
        if not isinstance(staff_data, dict):
            return []
            
        total_staff = int(staff_data.get('total_count', 0))
        base_efficiency = float(staff_data.get('efficiency', 0.8))
        
        shifts = staff_data.get('shifts', [
            {'shift': 'Mañana', 'staff_count': total_staff * 0.4, 'efficiency_score': base_efficiency},
            {'shift': 'Tarde', 'staff_count': total_staff * 0.35, 'efficiency_score': base_efficiency},
            {'shift': 'Noche', 'staff_count': total_staff * 0.25, 'efficiency_score': base_efficiency}
        ])
        
        return [
            {
                'label': shift['shift'],
                'value': shift['efficiency_score'] * 100,
                'staff_count': shift['staff_count']
            }
            for shift in shifts
        ]

    def _prepare_inventory_data(self, inventory_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepara datos de inventario para visualización"""
        if not isinstance(inventory_data, dict):
            return []
            
        data = []
        for item_name, item_info in inventory_data.items():
            if isinstance(item_info, dict):
                quantity = float(item_info.get('quantity', 0))
                min_stock = float(item_info.get('minimum_stock', 0))
                
                data.append({
                    'label': item_name.capitalize(),
                    'value': quantity,
                    'minimum': min_stock,
                    'status': 'OK' if quantity > min_stock else 'Low'
                })
        
        return sorted(data, key=lambda x: x['value'], reverse=True)

    def calculate_kpis(self, metrics: Dict[str, Any]) -> List[KPIMetric]:
        """Calcula los KPIs basados en las métricas"""
        kpis = []
        timestamp = datetime.now()
        
        # KPIs de ventas
        if 'sales' in metrics:
            sales = metrics['sales']
            total_sales = float(sales.get('total', 0))
            transactions = int(sales.get('transactions', 0))
            
            kpis.extend([
                KPIMetric(
                    name='sales_total',
                    value=total_sales,
                    trend=0.0,
                    target=self.kpi_thresholds['sales_total']['target'],
                    unit='CHF',
                    timestamp=timestamp
                ),
                KPIMetric(
                    name='average_ticket',
                    value=total_sales/transactions if transactions > 0 else 0,
                    trend=0.0,
                    target=100.0,
                    unit='CHF',
                    timestamp=timestamp
                )
            ])
        
        # KPIs de personal
        if 'staff' in metrics:
            staff = metrics['staff']
            efficiency = float(staff.get('efficiency', 0))
            satisfaction = float(staff.get('satisfaction', 0))
            
            kpis.extend([
                KPIMetric(
                    name='staff_efficiency',
                    value=efficiency * 100,
                    trend=0.0,
                    target=self.kpi_thresholds['staff_efficiency']['target'],
                    unit='%',
                    timestamp=timestamp
                ),
                KPIMetric(
                    name='staff_satisfaction',
                    value=satisfaction,
                    trend=0.0,
                    target=4.5,
                    unit='/5',
                    timestamp=timestamp
                )
            ])
        
        return kpis

    def generate_alerts(self, kpis: List[KPIMetric]) -> List[Alert]:
        """Genera alertas basadas en los KPIs"""
        alerts = []
        timestamp = datetime.now()
        
        for kpi in kpis:
            threshold = self.kpi_thresholds.get(kpi.name, {})
            if not threshold:
                continue
                
            if kpi.value <= threshold['critical']:
                alerts.append(Alert(
                    level='critical',
                    message=f"{kpi.name} está en nivel crítico: {kpi.value}{kpi.unit}",
                    source='kpi_monitor',
                    timestamp=timestamp
                ))
            elif kpi.value <= threshold['warning']:
                alerts.append(Alert(
                    level='warning',
                    message=f"{kpi.name} está bajo el objetivo: {kpi.value}{kpi.unit}",
                    source='kpi_monitor',
                    timestamp=timestamp
                ))
        
        return alerts

    def generate_recommendations(self, metrics: Dict[str, Any], kpis: List[KPIMetric], alerts: List[Alert]) -> List[str]:
        """Genera recomendaciones basadas en métricas y alertas"""
        recommendations = []
        
        # Recomendaciones basadas en KPIs
        for kpi in kpis:
            if kpi.target and kpi.value < kpi.target:
                if kpi.name == 'sales_total':
                    recommendations.append(
                        f"Aumentar ventas (actual: {kpi.value:,.2f} CHF, objetivo: {kpi.target:,.2f} CHF)"
                    )
                elif kpi.name == 'staff_efficiency':
                    recommendations.append(
                        f"Mejorar eficiencia del personal (actual: {kpi.value:.1f}%, objetivo: {kpi.target:.1f}%)"
                    )
                elif kpi.name == 'staff_satisfaction':
                    recommendations.append(
                        f"Mejorar satisfacción del personal (actual: {kpi.value:.1f}/5, objetivo: {kpi.target:.1f}/5)"
                    )
        
        # Recomendaciones basadas en métricas específicas
        if 'staff' in metrics:
            staff = metrics['staff']
            if staff.get('overtime_total', 0) > 20:
                recommendations.append(
                    "Optimizar planificación de turnos para reducir horas extra"
                )
            if staff.get('efficiency', 0) < 0.8:
                recommendations.append(
                    "Implementar programa de capacitación para mejorar eficiencia"
                )
        
        if 'inventory' in metrics:
            inventory = metrics['inventory']
            low_items = [
                item_name for item_name, item in inventory.items()
                if isinstance(item, dict) and item.get('quantity', 0) <= item.get('minimum_stock', 0)
            ]
            if low_items:
                recommendations.append(
                    f"Programar reposición inmediata de: {', '.join(low_items)}"
                )
        
        # Recomendaciones basadas en alertas críticas
        critical_alerts = [alert for alert in alerts if alert.level == 'critical']
        if len(critical_alerts) > 2:
            recommendations.append(
                "Atención inmediata requerida: múltiples métricas en estado crítico"
            )
        
        return recommendations

    def get_tools(self) -> List[StructuredTool]:
        """Retorna las herramientas disponibles para el agente"""
        return [
            StructuredTool.from_function(
                func=self.create_report,
                name="create_report",
                description="Crea un reporte completo con visualizaciones"
            ),
            StructuredTool.from_function(
                func=self.calculate_kpis,
                name="calculate_kpis",
                description="Calcula KPIs basados en métricas"
            ),
            StructuredTool.from_function(
                func=self.generate_alerts,
                name="generate_alerts",
                description="Genera alertas basadas en KPIs"
            ),
            StructuredTool.from_function(
                func=self.generate_recommendations,
                name="generate_recommendations",
                description="Genera recomendaciones basadas en métricas y alertas"
            )
        ]