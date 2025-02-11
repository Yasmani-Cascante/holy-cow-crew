#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import yaml
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
import pandas as pd
import numpy as np
import importlib.util

from .agents.performance_analysis_agent import PerformanceAnalysisAgent
from .agents.resource_optimization_agent import ResourceOptimizationAgent
from .agents.market_strategy_agent import MarketStrategyAgent
from .agents.reporting_agent import ReportingAgent

class TestRunner:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.root_dir = os.path.dirname(os.path.dirname(__file__))
        self.data_dir = os.path.join(self.root_dir, 'data')
        self.sample_dir = os.path.join(self.data_dir, 'sample')
        self.report_dir = os.path.join(self.data_dir, 'reports')
        os.makedirs(self.report_dir, exist_ok=True)

        self.config = self._load_config()
        self.inventory_catalog = self._load_inventory_catalog()
        self.agents = self._initialize_agents()

    def _load_config(self) -> Dict[str, Any]:
        config_path = os.path.join(self.data_dir, 'config.yaml')
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            raise

    def _load_inventory_catalog(self) -> Dict[str, Any]:
        catalog_path = os.path.join(
            self.sample_dir,
            self.config['data_sources']['inventory']['catalog']
        )
        try:
            spec = importlib.util.spec_from_file_location("catalog", catalog_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return {
                'items': module.INVENTORY_ITEMS,
                'recipes': module.BURGER_RECIPES
            }
        except Exception as e:
            self.logger.error(f"Error loading inventory catalog: {e}")
            raise

    def _initialize_agents(self) -> Dict[str, Any]:
        return {
            'performance': PerformanceAnalysisAgent(),
            'resources': ResourceOptimizationAgent(),
            'market': MarketStrategyAgent(),
            'reporting': ReportingAgent()
        }

    def _load_data(self, data_type: str) -> Dict[str, pd.DataFrame]:
        data_config = self.config['data_sources'][data_type]
        result = {}

        for key, filename in data_config.items():
            if key not in ['catalog']:
                try:
                    path = os.path.join(self.sample_dir, filename)
                    result[key] = pd.read_csv(path)
                except Exception as e:
                    self.logger.error(f"Error loading {data_type} - {key}: {e}")
                    raise

        return result

    def run_test(self) -> Optional[Tuple[Dict[str, Any], Dict[str, Any]]]:
        self.logger.info("Starting system test")
        
        try:
            data = {
                'inventory': self._load_data('inventory'),
                'sales': self._load_data('sales'),
                'support': self._load_data('support')
            }

            results = {}
            visualizations = {}

            for location in self.config['locations']:
                try:
                    location_data = self._prepare_location_data(location, data)
                    
                    # Análisis de rendimiento
                    perf_results = self.agents['performance'].analyze(
                        location_data,
                        self.config['analysis_config']
                    )
                    
                    # Optimización de recursos
                    resource_results = self.agents['resources'].optimize(
                        location_data,
                        perf_results,
                        self.inventory_catalog
                    )
                    
                    # Análisis de mercado
                    market_results = self.agents['market'].analyze(
                        location_data,
                        perf_results
                    )
                    
                    # Visualizaciones
                    viz = self.agents['reporting'].create_visualizations(
                        location,
                        perf_results,
                        resource_results,
                        market_results
                    )

                    results[location] = {
                        'performance': perf_results,
                        'resources': resource_results,
                        'market': market_results,
                        'status': 'success'
                    }
                    visualizations[location] = viz

                except Exception as e:
                    self.logger.error(f"Error processing {location}: {e}")
                    results[location] = {
                        'status': 'error',
                        'error': str(e)
                    }

            self._generate_report(results, visualizations)
            return results, visualizations

        except Exception as e:
            self.logger.error(f"Test execution failed: {e}")
            return None

    def _prepare_location_data(
        self,
        location: str,
        data: Dict[str, Dict[str, pd.DataFrame]]
    ) -> Dict[str, Any]:
        return {
            'inventory': {
                'current': data['inventory']['current'][
                    data['inventory']['current']['location'] == location
                ],
                'historical': data['inventory']['historical'][
                    data['inventory']['historical']['location'] == location
                ]
            },
            'sales': {
                'current': data['sales']['current'][
                    data['sales']['current']['location'] == location
                ],
                'historical': data['sales']['historical'][
                    data['sales']['historical']['location'] == location
                ]
            },
            'marketing': data['support']['marketing'][
                data['support']['marketing']['location'] == location
            ],
            'staff': data['support']['staff'][
                data['support']['staff']['location'] == location
            ]
        }

    def _generate_report(
        self,
        results: Dict[str, Any],
        visualizations: Dict[str, Any]
    ) -> None:
        try:
            report = self.agents['reporting'].generate_report(
                results,
                visualizations,
                self.config['analysis_config']
            )
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_path = os.path.join(self.report_dir, f'report_{timestamp}.md')
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
                
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            raise

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    logger = logging.getLogger(__name__)

    try:
        runner = TestRunner()
        results = runner.run_test()
        
        if results:
            logger.info("Test completed successfully")
            logger.info(f"Results saved in {runner.report_dir}")
        else:
            logger.error("Test failed")
            
    except Exception as e:
        logger.error(f"Error in main: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()