# Holy Cow! CrewAI Multi-Agent System

## Overview
This project implements a multi-agent system using CrewAI to optimize operations for the Holy Cow! restaurant chain in Switzerland. The system leverages existing sales prediction data to provide comprehensive resource optimization and business intelligence.

## System Architecture
The system consists of 8 specialized agents:

1. **Performance Analysis Agent**
   - Analyzes prediction accuracy
   - Calculates cost of errors
   - Provides insights for optimization

2. **Resource Optimization Agent**
   - Staff scheduling optimization
   - Inventory management
   - Dynamic promotion recommendations

3. **Reporting & Visualization Agent**
   - Adaptive dashboards
   - Intelligent alerting system
   - KPI monitoring

4. **Market Strategy Agent**
   - Promotion effectiveness analysis
   - Dynamic pricing recommendations
   - Market trend analysis

5. **Scenario Simulation Agent**
   - Impact analysis of strategies
   - Resource allocation modeling
   - Risk assessment

6. **Legal Compliance Agent**
   - Swiss labor law compliance
   - Food safety regulations
   - Canton-specific requirements

7. **Anomaly Detection Agent**
   - Real-time monitoring
   - Root cause analysis
   - Alert classification

8. **Feedback Integration Agent**
   - Recommendation validation
   - Model optimization
   - Learning from outcomes

## Project Structure
```
└── holy-cow-crew/
    ├── src/
    │   ├── agents/            # Individual agent implementations
    │   ├── tools/             # Custom tools for agents
    │   ├── models/            # Pydantic models
    │   └── flows/             # CrewAI flow definitions
    ├── config/                # Configuration files
    ├── tests/                 # Test suite
    ├── notebooks/             # Jupyter notebooks for analysis
    └── docs/                  # Documentation
```

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/Yasmani-Cascante/holy-cow-crew.git
cd holy-cow-crew

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration
Copy `.env.example` to `.env` and fill in your credentials:
```env
OPENAI_API_KEY=your_key_here
SERPER_API_KEY=your_key_here
# Add other required API keys
```

## Usage
Basic usage example:
```python
from holy_cow_crew.flows import RestaurantOptimizationFlow

flow = RestaurantOptimizationFlow()
results = flow.kickoff()
```

## Testing
```bash
python -m pytest tests/
```

## Contributing
Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
Yasmani Cascante - [GitHub Profile](https://github.com/Yasmani-Cascante)