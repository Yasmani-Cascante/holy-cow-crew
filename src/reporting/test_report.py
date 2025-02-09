from datetime import datetime
from typing import Dict, List
import json
import os
from pathlib import Path

class TestReportGenerator:
    def __init__(self, results: Dict):
        self.results = results
        self.timestamp = datetime.now()
    
    def format_currency(self, value: float) -> str:
        """Formatea valores monetarios en CHF"""
        return f"CHF {value:,.2f}"
    
    def generate_header(self) -> List[str]:
        """Genera el encabezado del reporte"""
        return [
            "# Reporte de Pruebas del Sistema Holy Cow",
            f"\nFecha de Generación: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            "\n## Resumen Ejecutivo",
            f"Total ubicaciones analizadas: {len(self.results)}",
            f"Análisis exitosos: {sum(1 for data in self.results.values() if data['success'])}",
            f"Análisis fallidos: {sum(1 for data in self.results.values() if not data['success'])}\n"
        ]
    
    def generate_location_section(self, location: str, data: Dict) -> List[str]:
        """Genera la sección de reporte para una ubicación específica"""
        section = [f"\n## Análisis: {location}"]
        
        if data['success']:
            metrics = data['metrics']
            
            # Métricas principales
            section.extend([
                "\n### Métricas Principales:",
                f"- Eficiencia Operativa: {metrics['efficiency']:.1f}%",
                f"- Ahorro Mensual Proyectado: {self.format_currency(metrics['savings'])}",
                f"- Ventas por Empleado: {self.format_currency(metrics['turnover_per_staff'])}",
                f"- Valor Total Inventario: {self.format_currency(metrics['inventory_value'])}"
            ])
            
            # Optimización de personal
            if metrics['recommended_staff'] is not None:
                current = metrics['current_staff']
                recommended = metrics['recommended_staff']
                diff = current - recommended
                direction = 'reducción' if diff > 0 else 'aumento'
                section.extend([
                    "\n### Optimización de Personal:",
                    f"- Personal Actual: {current} empleados",
                    f"- Personal Recomendado: {recommended} empleados",
                    f"- Cambio Sugerido: {abs(diff)} empleados ({direction})"
                ])
            
            # Si hay recomendaciones específicas
            if 'recommendations' in data:
                section.extend([
                    "\n### Recomendaciones Específicas:"
                ])
                section.extend([f"- {rec}" for rec in data['recommendations']])
            
            # KPIs adicionales si existen
            if 'kpis' in data:
                section.extend([
                    "\n### KPIs Adicionales:"
                ])
                for kpi_name, kpi_value in data['kpis'].items():
                    section.append(f"- {kpi_name}: {kpi_value}")
        else:
            section.extend([
                "\n### ⚠️ Error en el Análisis",
                f"Error: {data.get('error', 'Error desconocido')}",
                "\nDetalles adicionales del error:" if 'error_details' in data else "",
                f"{data.get('error_details', '')}"
            ])
        
        return section
    
    def generate_markdown_report(self) -> str:
        """Genera el reporte completo en formato Markdown"""
        report_sections = self.generate_header()
        
        # Agregar secciones por ubicación
        for location, data in self.results.items():
            report_sections.extend(self.generate_location_section(location, data))
        
        # Agregar timestamp y metadatos
        report_sections.extend([
            "\n## Metadatos del Reporte",
            f"- Generado el: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"- Total ubicaciones: {len(self.results)}",
            "- Versión del sistema: 1.0.0"  # Podrías obtener esto de una configuración
        ])
        
        return "\n".join(report_sections)
    
    def save_report(self, output_dir: str = "data/reports") -> str:
        """Guarda el reporte en formato Markdown y JSON"""
        # Crear directorio si no existe
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generar nombre de archivo con timestamp
        timestamp_str = self.timestamp.strftime("%Y%m%d_%H%M%S")
        base_filename = f"test_report_{timestamp_str}"
        
        # Guardar reporte Markdown
        md_path = os.path.join(output_dir, f"{base_filename}.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_markdown_report())
        
        # Guardar datos raw en JSON
        json_path = os.path.join(output_dir, f"{base_filename}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': self.timestamp.isoformat(),
                'results': self.results
            }, f, indent=2, ensure_ascii=False)
        
        return md_path