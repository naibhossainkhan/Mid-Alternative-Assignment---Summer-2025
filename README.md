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
python main.py install
# or
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Using the Main Launcher (Recommended)
```bash
# Run Streamlit app (simple version)
python main.py streamlit --simple

# Run Streamlit app (full version - requires API key)
python main.py streamlit

# Run demo workflow
python main.py demo --simple

# Run tests
python main.py test
```

#### Option 2: Direct Commands
```bash
# Streamlit apps
streamlit run streamlit/streamlit_app_simple.py
streamlit run streamlit/streamlit_app.py

# Demo scripts
python demos/demo_agentic_workflow_simple.py
python demos/demo_agentic_workflow.py
```

## 📁 Project Structure

```
├── main.py                 # Main entry point with CLI
├── run.py                  # Simple launcher
├── requirements.txt        # Python dependencies
├── config.py              # Configuration settings
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── Makefile               # Build and deployment commands
├── .gitignore            # Git ignore rules
├── env.example           # Environment variables template
│
├── src/                  # Core source code
│   ├── __init__.py
│   ├── customer_data_loader.py    # Data loading and preprocessing
│   ├── visualization.py           # Chart generation
│   ├── narrative_generator.py     # AI insights generation
│   ├── customer_ai_agent.py       # LangChain AI agent
│   └── ai_provider.py             # AI service providers
│
├── streamlit/            # Streamlit web applications
│   ├── __init__.py
│   ├── streamlit_app_simple.py    # Simple version (no LangChain)
│   └── streamlit_app.py           # Full version (with LangChain)
│
├── demos/                # Demonstration scripts
│   ├── __init__.py
│   ├── demo_agentic_workflow_simple.py
│   ├── demo_agentic_workflow.py
│   ├── demo_multi_model_ai.py
│   ├── demo_multi_model_simple.py
│   ├── demo_textual_summary.py
│   ├── demo_textual_summary_simple.py
│   ├── customer_demo.py
│   └── customer_demo_simple.py
│
├── tests/                # Test suite
│   ├── __init__.py
│   └── test_installation.py
│
├── data/                 # Data files
│   └── customer_shopping_data.csv
│
├── docs/                 # Documentation
│   ├── README.md         # This file
│   ├── summaries/        # Project summaries
│   │   ├── AGENTIC_WORKFLOW_SUMMARY.md
│   │   ├── MULTI_MODEL_AI_SUMMARY.md
│   │   ├── CUSTOMER_SHOPPING_SUMMARY.md
│   │   ├── ASSIGNMENT_SUMMARY.md
│   │   └── CLEANUP_SUMMARY.md
│   ├── guides/           # User guides
│   │   ├── SUBMISSION_GUIDE.md
│   │   └── TROUBLESHOOTING.md
│   ├── api/              # API documentation
│   ├── deployment/       # Deployment guides
│   └── user_guide/       # User documentation
│
├── notebooks/            # Jupyter notebooks
│   ├── data_exploration.ipynb
│   └── agentic_workflow.ipynb
│
├── app/                  # Alternative app structure
│   ├── main.py
│   ├── config/
│   ├── core/
│   ├── services/
│   ├── utils/
│   ├── static/
│   ├── templates/
│   └── tests/
│
├── static/               # Static assets
├── screenshots/          # Application screenshots
├── deployment/           # Deployment configurations
└── scripts/              # Utility scripts
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
python main.py test

# Run specific test
python tests/test_installation.py
```

### Code Quality
```bash
# Format code
black src/ demos/ streamlit/ tests/

# Lint code
flake8 src/ demos/ streamlit/ tests/

# Type checking
mypy src/ demos/ streamlit/ tests/
```

## 🚀 Deployment

### Local Development
```bash
# Run with auto-reload
streamlit run streamlit/streamlit_app_simple.py --server.runOnSave true
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
# Using Makefile
make deploy

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
3. Run the test suite: `python main.py test`

---

**Data Visualization Assignment - Summer 2025**  
*AI-Powered Customer Shopping Analytics Platform*
