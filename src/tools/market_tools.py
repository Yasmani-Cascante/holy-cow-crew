from langchain.tools import StructuredTool, tool
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from ..models.market_models import LocalEvent, CantonInfo, MarketingRecommendation

class MarketTools:
    def __init__(self):
        # Base de datos simplificada de eventos conocidos en Suiza
        self.swiss_events = {
            'Zurich': [
                ('Züri Fäscht', 'July', 2000000, 'cultural'),
                ('Street Parade', 'August', 1000000, 'entertainment'),
                ('Sechseläuten', 'April', 50000, 'traditional')
            ],
            'Geneva': [
                ('Geneva Motor Show', 'March', 600000, 'business'),
                ('Fêtes de Genève', 'August', 500000, 'cultural'),
                ("L'Escalade", 'December', 30000, 'traditional')
            ],
            'Basel': [
                ('Fasnacht', 'February', 200000, 'cultural'),
                ('Art Basel', 'June', 100000, 'cultural'),
                ('Basel Autumn Fair', 'October', 500000, 'entertainment')
            ]
        }
        
        # Datos demográficos por cantón
        self.canton_data = {
            'Zurich': {
                'language': 'German',
                'population': 1520968,
                'key_demographics': {
                    'young_professionals': 0.35,
                    'families': 0.40,
                    'students': 0.15,
                    'tourists': 0.10
                }
            },
            'Geneva': {
                'language': 'French',
                'population': 499332,
                'key_demographics': {
                    'international_community': 0.30,
                    'business_professionals': 0.35,
                    'locals': 0.25,
                    'tourists': 0.10
                }
            },
            'Basel': {
                'language': 'German',
                'population': 194766,
                'key_demographics': {
                    'urban_professionals': 0.30,
                    'cultural_enthusiasts': 0.25,
                    'students': 0.20,
                    'families': 0.25
                }
            }
        }

    def analyze_local_events(self, location: str, date_range: Tuple[str, str]) -> List[LocalEvent]:
        """
        Analiza eventos locales para oportunidades de marketing
        
        Args:
            location: Ciudad/cantón objetivo
            date_range: (fecha_inicio, fecha_fin) en formato 'YYYY-MM-DD'
        
        Returns:
            Lista de eventos relevantes
        """
        events = []
        start_date = datetime.strptime(date_range[0], '%Y-%m-%d')
        end_date = datetime.strptime(date_range[1], '%Y-%m-%d')
        
        if location in self.swiss_events:
            for event_name, month, attendance, category in self.swiss_events[location]:
                event_date = datetime.strptime(f"2025-{month}-01", '%Y-%B-%d')
                if start_date <= event_date <= end_date:
                    events.append(LocalEvent(
                        name=event_name,
                        date=event_date.strftime('%Y-%m-%d'),
                        location=location,
                        expected_attendance=attendance,
                        category=category
                    ))
        
        return events

    def analyze_canton_demographics(self, canton: str) -> CantonInfo:
        """
        Analiza demografía y preferencias específicas del cantón
        
        Args:
            canton: Nombre del cantón
            
        Returns:
            Información demográfica del cantón
        """
        if canton in self.canton_data:
            data = self.canton_data[canton]
            return CantonInfo(
                name=canton,
                language=data['language'],
                population=data['population'],
                key_demographics=data['key_demographics']
            )
        else:
            raise ValueError(f"No data available for canton: {canton}")

    def generate_recommendations(self, 
                               events: List[LocalEvent], 
                               demographics: CantonInfo) -> List[MarketingRecommendation]:
        """
        Genera recomendaciones de marketing específicas para el cantón
        
        Args:
            events: Lista de eventos locales
            demographics: Información demográfica del cantón
            
        Returns:
            Lista de recomendaciones de marketing
        """
        recommendations = []
        
        # Identificar segmentos principales
        main_segments = sorted(
            demographics.key_demographics.items(),
            key=lambda x: x[1],
            reverse=True
        )[:2]
        
        for event in events:
            # Generar recomendación basada en tipo de evento
            if event.category == 'cultural':
                campaign_type = 'Local Heritage'
                target = main_segments[0][0]
            elif event.category == 'business':
                campaign_type = 'Professional Networking'
                target = 'business_professionals'
            else:
                campaign_type = 'Community Event'
                target = main_segments[1][0]
            
            # Calcular impacto esperado basado en asistencia al evento
            expected_impact = {
                'brand_awareness': min(event.expected_attendance / 10000, 100),
                'engagement_rate': min(event.expected_attendance / 20000, 100),
                'estimated_visits': event.expected_attendance * 0.05
            }
            
            recommendations.append(MarketingRecommendation(
                target_location=demographics.name,
                campaign_type=campaign_type,
                timing=f"During {event.name}",
                target_audience=target,
                expected_impact=expected_impact
            ))
        
        return recommendations

    def get_tools(self) -> List[StructuredTool]:
        """Retorna las herramientas disponibles para análisis de mercado"""
        return [
            StructuredTool.from_function(
                func=self.analyze_local_events,
                name="analyze_local_events",
                description="Analyze local events for marketing opportunities"
            ),
            StructuredTool.from_function(
                func=self.analyze_canton_demographics,
                name="analyze_canton_demographics",
                description="Analyze canton demographics and preferences"
            ),
            StructuredTool.from_function(
                func=self.generate_recommendations,
                name="generate_recommendations",
                description="Generate location-specific marketing recommendations"
            )
        ]