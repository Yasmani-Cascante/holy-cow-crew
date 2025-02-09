"""Datos de ejemplo para pruebas del sistema"""

test_data = {
    "Zurich": {
        "sales_data": {
            "predicted_sales": 15000,
            "current_staff": 15,
            "inventory_levels": {
                "meat": 4.5,
                "vegetables": 3.2,
                "dairy": 5.0,
                "dry_goods": 18.0
            },
            "peak_hours": ["12:00", "13:00", "19:00", "20:00"],
            "sales_growth": {
                "current": 15000,
                "previous": 14200,
                "growth_rate": 5.63
            }
        },
        "market_data": {
            "local_events": [
                {
                    "name": "Zurich Film Festival",
                    "date": "2025-03-15",
                    "expected_attendance": 5000
                },
                {
                    "name": "Street Food Festival",
                    "date": "2025-03-20",
                    "expected_attendance": 3000
                }
            ],
            "demographics": {
                "average_age": 35,
                "income_level": "high",
                "business_district": True
            }
        }
    },
    "Geneva": {
        "sales_data": {
            "predicted_sales": 12000,
            "current_staff": 12,
            "inventory_levels": {
                "meat": 3.8,
                "vegetables": 2.5,
                "dairy": 4.2,
                "dry_goods": 15.0
            },
            "peak_hours": ["12:30", "13:30", "19:30", "20:30"],
            "sales_growth": {
                "current": 12000,
                "previous": 11500,
                "growth_rate": 4.35
            }
        },
        "market_data": {
            "local_events": [
                {
                    "name": "Geneva Motor Show",
                    "date": "2025-03-25",
                    "expected_attendance": 8000
                }
            ],
            "demographics": {
                "average_age": 40,
                "income_level": "very_high",
                "business_district": True
            }
        }
    },
    "Basel": {
        "sales_data": {
            "predicted_sales": 10000,
            "current_staff": 10,
            "inventory_levels": {
                "meat": 3.0,
                "vegetables": 2.0,
                "dairy": 3.5,
                "dry_goods": 12.0
            },
            "peak_hours": ["12:00", "13:00", "18:30", "19:30"],
            "sales_growth": {
                "current": 10000,
                "previous": 9800,
                "growth_rate": 2.04
            }
        },
        "market_data": {
            "local_events": [
                {
                    "name": "Art Basel",
                    "date": "2025-03-10",
                    "expected_attendance": 6000
                }
            ],
            "demographics": {
                "average_age": 38,
                "income_level": "high",
                "business_district": False
            }
        }
    }
}