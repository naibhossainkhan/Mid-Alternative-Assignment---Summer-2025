# AI-Powered Customer Shopping Analytics

A comprehensive data visualization and analytics platform that demonstrates Agentic AI workflows for customer shopping data analysis.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd "Mid Alternative Assignment - Summer 2025"

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Streamlit Web App (Recommended)
```bash
# Run the main Streamlit application
streamlit run streamlit_app.py
```

#### Option 2: Demo Scripts
```bash
# Run AI workflow demo
python demos/demo_agentic_workflow.py

# Run simple demo
python demos/demo_agentic_workflow_simple.py

# Run multi-model AI demo
python demos/demo_multi_model_ai.py
```

#### Option 3: Using the Launcher
```bash
# Run Streamlit app
python run.py streamlit

# Run demo
python run.py demo

# Run tests
python run.py test
```

## 📁 Project Structure

```
├── README.md                    # Project documentation
├── requirements.txt             # Main dependencies
├── requirements-simple.txt      # Minimal dependencies
├── run.py                       # Application launcher
├── config.py                    # Configuration settings
├── .env                         # Environment variables
├── .streamlit/                  # Streamlit configuration
│   ├── config.toml             # Streamlit settings
│   └── secrets.toml            # API keys (not in git)
├── .gitignore                  # Git ignore rules
├── env.example                 # Environment template
│
├── core/                       # Core application modules
│   ├── __init__.py
│   ├── data/                   # Data handling
│   │   ├── __init__.py
│   │   ├── loader.py           # Data loading and preprocessing
│   │   └── processor.py        # Data processing utilities
│   ├── ai/                     # AI and ML components
│   │   ├── __init__.py
│   │   ├── agent.py            # LangChain AI agent
│   │   ├── generator.py        # AI narrative generation
│   │   └── provider.py         # AI service providers
│   ├── visualization/          # Visualization components
│   │   ├── __init__.py
│   │   ├── charts.py           # Chart generation
│   │   └── dashboard.py        # Dashboard components
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── config.py           # Configuration utilities
│       └── helpers.py          # Helper functions
│
├── streamlit_app.py            # Main Streamlit application
│
├── demos/                      # Demonstration scripts
│   ├── __init__.py
│   ├── demo_agentic_workflow.py
│   ├── demo_agentic_workflow_simple.py
│   ├── demo_multi_model_ai.py
│   ├── demo_multi_model_simple.py
│   ├── demo_textual_summary.py
│   ├── demo_textual_summary_simple.py
│   ├── customer_demo.py
│   └── customer_demo_simple.py
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_core/              # Core module tests
│   │   ├── test_data.py
│   │   ├── test_ai.py
│   │   └── test_visualization.py
│   ├── test_integration/       # Integration tests
│   └── test_streamlit/         # Streamlit app tests
│
├── data/                       # Data files
│   └── customer_shopping_data.csv
│
├── docs/                       # Documentation
│   ├── api/                    # API documentation
│   ├── deployment/             # Deployment guides
│   ├── guides/                 # User guides
│   ├── summaries/              # Project summaries
│   └── user_guide/             # User documentation
│
├── notebooks/                  # Jupyter notebooks
│   ├── data_exploration.ipynb
│   └── agentic_workflow.ipynb
│
├── static/                     # Static assets
│   ├── css/
│   ├── js/
│   └── images/
│
├── deployment/                 # Deployment configurations
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── scripts/
│
├── screenshots/                # Application screenshots
└── scripts/                    # Utility scripts
```

## 🎯 Features

### Core Functionality
- **Natural Language Query Processing**: Convert human queries to structured data operations
- **Automated Data Visualization**: Generate charts and graphs automatically
- **AI-Powered Insights**: Intelligent data interpretation and narrative generation
- **Interactive Dashboard**: Web-based interface for data exploration

### Data Analysis Capabilities
- Customer spending patterns by category
- Revenue trends over time
- Gender and age group analysis
- Shopping mall performance
- Payment method preferences
- Seasonal spending patterns

### Visualization Types
- Bar charts
- Line charts
- Pie charts
- Scatter plots
- Heatmaps
- Time series analysis

## 🤖 AI Components

### Agentic AI Workflow
- **Query Translation**: Natural language to Pandas operations
- **Data Processing**: Automated data cleaning and transformation
- **Visualization Generation**: Context-aware chart creation
- **Insight Generation**: AI-powered data interpretation

### AI Models
- **Local Mode**: Rule-based processing (no API required)
- **OpenAI Integration**: GPT-based natural language processing
- **Google AI**: Alternative AI provider support
- **LangChain**: Agent framework for complex workflows

## 📊 Data

The application uses a comprehensive customer shopping dataset with:
- **99,457 records** of customer transactions
- **18 features** including demographics, products, and transactions
- **Multiple categories** of products and shopping malls
- **Time-series data** for trend analysis

## 🛠️ Development

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp env.example .env
# Edit .env with your API keys
```

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test category
python -m pytest tests/test_core/
python -m pytest tests/test_integration/
```

### Code Quality
```bash
# Format code
black core/ demos/ tests/

# Lint code
flake8 core/ demos/ tests/

# Type checking
mypy core/ demos/ tests/
```

## 🚀 Deployment

### Local Development
```bash
# Run with auto-reload
streamlit run streamlit_app.py --server.runOnSave true
```

### Docker Deployment
```bash
# Build and run with Docker
docker-compose up --build

# Or build manually
docker build -t customer-analytics .
docker run -p 8501:8501 customer-analytics
```

### Production Deployment
```bash
# Using deployment scripts
./deployment/scripts/deploy.sh

# Manual deployment
gunicorn -w 4 -b 0.0.0.0:8501 streamlit_app:app
```

## 📚 Documentation

- **[Assignment Summary](docs/summaries/ASSIGNMENT_SUMMARY.md)**: Complete assignment overview
- **[Agentic Workflow](docs/summaries/AGENTIC_WORKFLOW_SUMMARY.md)**: AI workflow implementation
- **[Submission Guide](docs/guides/SUBMISSION_GUIDE.md)**: How to submit the assignment
- **[Troubleshooting](docs/guides/TROUBLESHOOTING.md)**: Common issues and solutions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is part of the Data Visualization Assignment for Summer 2025.

## 🆘 Support

For issues and questions:
1. Check the [Troubleshooting Guide](docs/guides/TROUBLESHOOTING.md)
2. Review the [Documentation](docs/)
3. Run the test suite: `python -m pytest tests/`

---

**Data Visualization Assignment - Summer 2025**  
*AI-Powered Customer Shopping Analytics Platform*
