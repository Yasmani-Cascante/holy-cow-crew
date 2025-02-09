from typing import Dict, List, Any, Tuple, Union
from datetime import datetime, date
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool

class LocalEvent(BaseModel):
    name: str
    date: str
    expected_attendance: int
    type: str
    location: str

class CantonInfo(BaseModel):
    name: str
    language: str
    population: int
    key_demographics: Dict[str, float]

class MarketingTools:
    """Herramientas para análisis de marketing y generación de recomendaciones"""

    def analyze_local_events(self, location: str, date_range: Union[List[str], Tuple[str, str]]) -> List[Dict]:
        """
        Analyze local events for marketing opportunities.
        Args:
            location (str): Location name
            date_range (Union[List[str], Tuple[str, str]]): Start and end date as ["YYYY-MM-DD", "YYYY-MM-DD"] or ("YYYY-MM-DD", "YYYY-MM-DD")
        """
        # Convert list to tuple if necessary
        if isinstance(date_range, list):
            date_range = tuple(date_range)
        
        # Mock implementation for different locations
        events = {
            "Zurich": [{
                "name": "Zurich Food Festival",
                "date": date_range[0],
                "expected_attendance": 5000,
                "type": "Food",
                "location": "Zurich"
            }],
            "Geneva": [{
                "name": "Geneva International Motor Show",
                "date": date_range[0],
                "expected_attendance": 8000,
                "type": "Auto",
                "location": "Geneva"
            }],
            "Basel": [{
                "name": "Art Basel",
                "date": date_range[0],
                "expected_attendance": 6000,
                "type": "Art",
                "location": "Basel"
            }]
        }
        
        return events.get(location, [])

    def analyze_canton_demographics(self, canton: str) -> Dict:
        """
        Analyze canton demographics and return formatted data
        Args:
            canton (str): Canton name
        """
        demographics = {
            "Zurich": {
                "name": "Zurich",
                "language": "German",
                "population": 1520968,
                "key_demographics": {
                    "young_professionals": 0.35,
                    "families": 0.4,
                    "students": 0.15,
                    "tourists": 0.1
                }
            },
            "Geneva": {
                "name": "Geneva",
                "language": "French",
                "population": 499480,
                "key_demographics": {
                    "young_professionals": 0.30,
                    "families": 0.35,
                    "students": 0.20,
                    "tourists": 0.15
                }
            },
            "Basel": {
                "name": "Basel",
                "language": "German",
                "population": 194766,
                "key_demographics": {
                    "young_professionals": 0.25,
                    "families": 0.30,
                    "students": 0.25,
                    "tourists": 0.20
                }
            }
        }
        return demographics.get(canton, {"error": "Canton not found"})

    def generate_recommendations(self, events: List[Dict], demographics: Dict) -> Dict:
        """
        Generate marketing recommendations based on events and demographics
        Args:
            events (List[Dict]): List of local events
            demographics (Dict): Canton demographic information including key_demographics
        """
        try:
            # Ensure demographics has the correct format
            canton_info = CantonInfo(**demographics)
            
            recommendations = {
                "target_segments": [],
                "channels": [],
                "tactics": []
            }
            
            # Process demographic insights
            kd = canton_info.key_demographics
            if kd.get("young_professionals", 0) >= 0.3:
                recommendations["target_segments"].append("Young Professionals")
                recommendations["channels"].extend(["Instagram", "LinkedIn"])
                recommendations["tactics"].append({
                    "segment": "Young Professionals",
                    "action": "After-work special deals",
                    "details": "Create exclusive evening promotions targeting young professionals"
                })
            
            if kd.get("families", 0) >= 0.3:
                recommendations["target_segments"].append("Families")
                recommendations["channels"].extend(["Facebook", "Local Radio"])
                recommendations["tactics"].append({
                    "segment": "Families",
                    "action": "Weekend family bundles",
                    "details": "Design value-packed family meals and kids-eat-free promotions"
                })
            
            if kd.get("students", 0) >= 0.1:
                recommendations["target_segments"].append("Students")
                recommendations["channels"].append("Instagram")
                recommendations["tactics"].append({
                    "segment": "Students",
                    "action": "Student discounts",
                    "details": "Implement student ID discounts and group deals"
                })
            
            # Process event insights
            for event in events:
                if event["expected_attendance"] > 1000:
                    recommendations["tactics"].append({
                        "segment": "Event Attendees",
                        "action": f"Special promotion during {event['name']}",
                        "details": f"Create themed menu items and promotions aligned with {event['name']}"
                    })
            
            return recommendations
        except Exception as e:
            print(f"Error in generate_recommendations: {str(e)}")
            return {"error": f"Failed to generate recommendations: {str(e)}"}

    def get_tools(self) -> List[StructuredTool]:
        """Get all marketing tools"""
        return [
            StructuredTool.from_function(
                func=self.analyze_local_events,
                name="analyze_local_events",
                description="Analyze local events for marketing opportunities",
            ),
            StructuredTool.from_function(
                func=self.analyze_canton_demographics,
                name="analyze_canton_demographics",
                description="Analyze canton demographics"
            ),
            StructuredTool.from_function(
                func=self.generate_recommendations,
                name="generate_recommendations",
                description="Generate location-specific marketing recommendations"
            )
        ]