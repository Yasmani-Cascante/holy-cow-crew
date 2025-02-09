from crewai import Agent, Task, Crew, Process
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from src.integrator import HolyCowIntegrator
from src.agents.reporting_agent import ReportingAgent
import pandas as pd
import numpy as np
import json
import os

def load_test_data():
    """Carga datos de prueba desde archivos CSV"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data', 'sample')
    
    # Cargar datos de ventas
    sales_df = pd.read_csv(os.path.join(data_dir, 'sales_history.csv'))
    sales_by_location = {
        location: location_data for location, location_data in sales_df.groupby('location')
    }
    
    # Datos de inventario
    try:
        inventory_df = pd.read_csv(os.path.join(data_dir, 'inventory.csv'))
        inventory_data = {}
        for _, row in inventory_df.iterrows():
            if row['location'] not in inventory_data:
                inventory_data[row['location']] = {}
            inventory_data[row['location']][row['item']] = {
                'quantity': row['quantity'],
                'minimum_stock': row['minimum_stock'],
                'cost_per_unit': row['cost_per_unit'],
                'last_restock_date': row['last_restock_date'],
                'expiry_date': row['expiry_date'],
                'supplier': row['supplier']
            }
    except Exception as e:
        print(f"Usando datos de inventario por defecto: {str(e)}")
        inventory_data = {
            'Zurich': {'meat': 5.0, 'vegetables': 3.0, 'dairy': 4.0},
            'Geneva': {'meat': 4.0, 'vegetables': 2.0, 'dairy': 3.0},
            'Basel': {'meat': 6.0, 'vegetables': 4.0, 'dairy': 5.0}
        }
    
    # Datos de personal
    try:
        staff_df = pd.read_csv(os.path.join(data_dir, 'staff_metrics.csv'))
        staff_data = {}
        for location, group in staff_df.groupby('location'):
            staff_data[location] = {
                'total_count': group['staff_count'].sum(),
                'efficiency': group['efficiency_score'].mean(),
                'satisfaction': group['customer_satisfaction'].mean(),
                'experience': group['years_experience'].mean(),
                'shifts': group[['shift', 'staff_count', 'efficiency_score']].to_dict('records'),
                'overtime_total': group['overtime_hours'].sum()
            }
    except Exception as e:
        print(f"Usando datos de personal por defecto: {str(e)}")
        staff_data = {
            'Zurich': {'total_count': 12},
            'Geneva': {'total_count': 10},
            'Basel': {'total_count': 8}
        }
    
    return sales_by_location, inventory_data, staff_data

def format_currency(value: float) -> str:
    """Formatea valores monetarios"""
    return f"CHF {value:,.2f}"

def generate_enhanced_report(results: Dict[str, Any], visualizations: Dict[str, Any]) -> str:
    """Genera un reporte detallado con todos los análisis y visualizaciones"""
    report_lines = [
        "# Reporte de Análisis - Holy Cow!",
        f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        "## Resumen Ejecutivo\n"
    ]
    
    # Métricas globales
    total_sales = sum(
        data['metrics']['sales']['total'] 
        for data in results.values() 
        if data['success']
    )
    total_staff = sum(
        data['metrics']['staff'].get('total_count', 0)
        for data in results.values() 
        if data['success']
    )
    
    report_lines.extend([
        f"Ventas Totales Red: {format_currency(total_sales)}",
        f"Personal Total: {total_staff} empleados",
        f"Ubicaciones Analizadas: {len(results)}\n",
        "## Análisis por Ubicación\n"
    ])
    
    # Análisis por ubicación
    for location, data in results.items():
        report_lines.append(f"### {location}")
        
        if data['success']:
            metrics = data['metrics']
            analysis = data.get('analysis', {})
            
            # Sección de Ventas
            report_lines.extend([
                "\n#### 📈 Rendimiento en Ventas",
                f"- Ventas Totales: {format_currency(metrics['sales']['total'])}",
                f"- Transacciones: {metrics['sales'].get('transactions', 0)}",
                f"- Ticket Promedio: {format_currency(metrics['sales']['total'] / metrics['sales'].get('transactions', 1))}",
                "\nTendencias de Ventas:",
                "```\n" + visualizations.get(f"{location}_sales_hourly", "No hay datos disponibles") + "\n```"
            ])
            
            # Sección de Personal
            report_lines.extend([
                "\n#### 👥 Gestión de Personal",
                f"- Total Empleados: {metrics['staff'].get('total_count', 0)}",
                f"- Eficiencia: {metrics['staff'].get('efficiency', 0) * 100:.1f}%",
                f"- Satisfacción Cliente: {metrics['staff'].get('satisfaction', 0):.1f}/5.0",
                f"- Horas Extra: {metrics['staff'].get('overtime_total', 0):.1f}h",
                "\nEficiencia por Turno:",
                "```\n" + visualizations.get(f"{location}_staff_efficiency", "No hay datos disponibles") + "\n```"
            ])
            
            # Sección de Inventario
            inventory_metrics = metrics.get('inventory', {})
            report_lines.extend([
                "\n#### 📦 Gestión de Inventario",
                f"- Items Totales: {len(inventory_metrics)}",
                f"- Items Bajo Mínimo: {sum(1 for item in inventory_metrics.values() if item.get('quantity', 0) <= item.get('minimum_stock', 0))}",
                f"- Valor Total: {format_currency(sum(item.get('quantity', 0) * item.get('cost_per_unit', 0) for item in inventory_metrics.values()))}",
                "\nNiveles de Inventario:",
                "```\n" + visualizations.get(f"{location}_inventory_levels", "No hay datos disponibles") + "\n```"
            ])
            
            # Recomendaciones y Alertas
            if 'alerts' in analysis:
                report_lines.extend([
                    "\n#### ⚠️ Alertas",
                    *[f"- {alert}" for alert in analysis['alerts']]
                ])
            
            if 'recommendations' in analysis:
                report_lines.extend([
                    "\n#### 💡 Recomendaciones",
                    *[f"- {rec}" for rec in analysis['recommendations']]
                ])
            
        else:
            report_lines.extend([
                "\n⚠️ Error en el Análisis",
                f"Error: {data.get('error', 'Error desconocido')}"
            ])
        
        report_lines.append("\n---\n")
    
    return "\n".join(report_lines)

def run_restaurant_optimization():
    """Ejecuta el análisis completo del restaurante"""
    integrator = HolyCowIntegrator()
    reporting_agent = ReportingAgent()
    
    print("Cargando datos...")
    sales_data, inventory_data, staff_data = load_test_data()
    
    results = {}
    visualizations = {}
    locations = ['Zurich', 'Geneva', 'Basel']
    
    for location in locations:
        print(f"\n{'='*20} Análisis: {location} {'='*20}")
        
        try:
            # Preparar datos
            location_sales = sales_data.get(location, pd.DataFrame())
            metrics = {
                'sales': {
                    'total': float(location_sales['total_sales'].sum()) if not location_sales.empty else 0,
                    'transactions': int(location_sales['transactions'].sum()) if not location_sales.empty else 0,
                    'peak_hours': location_sales.groupby('peak_hour')['total_sales'].sum().nlargest(3).index.tolist() if not location_sales.empty else []
                },
                'inventory': inventory_data.get(location, {}),
                'staff': staff_data.get(location, {'total_count': 0})
            }
            
            # Mostrar métricas clave
            print("\nMétricas Principales:")
            print(f"- Ventas: {format_currency(metrics['sales']['total'])}")
            print(f"- Personal: {metrics['staff']['total_count']} empleados")
            
            # Ejecutar análisis
            analysis = integrator.analyze_location(location, metrics)
            
            # Generar visualizaciones
            report_result = reporting_agent.create_report(location, metrics)
            if report_result['success']:
                visualizations.update({
                    f"{location}_{key}": value 
                    for key, value in report_result['visualizations'].items()
                })
            
            # Guardar resultados
            results[location] = {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'metrics': metrics,
                'analysis': analysis
            }
            
        except Exception as e:
            print(f"\nError en análisis de {location}: {str(e)}")
            import traceback
            results[location] = {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
    
    # Generar reporte
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_content = generate_enhanced_report(results, visualizations)
    
    # Guardar resultados
    os.makedirs('data/reports', exist_ok=True)
    
    # Reporte detallado
    report_file = f'data/reports/analysis_report_{timestamp}.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    # Datos raw en JSON
    results_file = f'data/reports/analysis_data_{timestamp}.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nReporte generado en: {report_file}")
    print(f"Datos guardados en: {results_file}")
    
    return results, report_content

if __name__ == "__main__":
    print("\nIniciando análisis completo del sistema...")
    try:
        results, report = run_restaurant_optimization()
        print("\nAnálisis completado exitosamente")
        print("\nContenido del Reporte:")
        print(report)
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")
        import traceback
        traceback.print_exc()