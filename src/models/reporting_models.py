from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ChartConfig(BaseModel):
    """Configuración para gráficos"""
    type: str = Field(..., description="Tipo de gráfico (line, bar, pie, etc.)")
    title: str = Field(..., description="Título del gráfico")
    data_key: str = Field(..., description="Clave para los datos")
    x_axis: str = Field(..., description="Campo para eje X")
    y_axis: str = Field(..., description="Campo para eje Y")
    color_scheme: List[str] = Field(default=["#8884d8", "#82ca9d", "#ffc658"])
    width: int = Field(default=600)
    height: int = Field(default=400)
    show_grid: bool = Field(default=True)
    show_tooltip: bool = Field(default=True)
    show_legend: bool = Field(default=True)

class KPIMetric(BaseModel):
    """Métrica de KPI"""
    name: str = Field(..., description="Nombre del KPI")
    value: float = Field(..., description="Valor actual")
    trend: float = Field(..., description="Tendencia (cambio vs período anterior)")
    target: Optional[float] = Field(None, description="Valor objetivo")
    unit: str = Field(..., description="Unidad de medida")
    timestamp: datetime = Field(..., description="Momento de la medición")

class Alert(BaseModel):
    """Alerta del sistema"""
    level: str = Field(..., description="Nivel de alerta (warning, critical)")
    message: str = Field(..., description="Mensaje de la alerta")
    source: str = Field(..., description="Fuente de la alerta")
    timestamp: datetime = Field(..., description="Momento de la alerta")
    acknowledged: bool = Field(default=False, description="Si la alerta ha sido reconocida")

class DashboardWidget(BaseModel):
    """Widget individual del dashboard"""
    id: str = Field(..., description="Identificador único del widget")
    type: str = Field(..., description="Tipo de widget (chart, metrics, etc.)")
    title: str = Field(..., description="Título del widget")
    data_source: str = Field(..., description="Fuente de datos")
    position: Dict[str, int] = Field(..., description="Posición en el dashboard")
    config: Optional[ChartConfig] = None
    refresh_interval: int = Field(default=300, description="Intervalo de actualización en segundos")

class DashboardConfig(BaseModel):
    """Configuración completa del dashboard"""
    title: str = Field(..., description="Título del dashboard")
    layout: Dict[str, Any] = Field(..., description="Configuración del layout")
    widgets: List[DashboardWidget] = Field(..., description="Lista de widgets")
    refresh_rate: int = Field(default=300, description="Tasa de actualización global")
    theme: str = Field(default="light", description="Tema del dashboard")

class ReportSection(BaseModel):
    """Sección de un reporte"""
    title: str = Field(..., description="Título de la sección")
    content: str = Field(..., description="Contenido principal")
    charts: List[ChartConfig] = Field(default=[], description="Gráficos de la sección")
    kpis: List[KPIMetric] = Field(default=[], description="KPIs de la sección")
    alerts: List[Alert] = Field(default=[], description="Alertas de la sección")

class Report(BaseModel):
    """Reporte completo"""
    title: str = Field(..., description="Título del reporte")
    timestamp: datetime = Field(..., description="Momento de generación")
    location: str = Field(..., description="Ubicación analizada")
    sections: List[ReportSection] = Field(..., description="Secciones del reporte")
    summary: str = Field(..., description="Resumen ejecutivo")
    recommendations: List[str] = Field(..., description="Recomendaciones")