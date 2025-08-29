# AI-Powered Customer Shopping Analytics

A production-grade Streamlit application for data analytics and visualization using Generative and Agentic AI technologies.

## 🚀 Features

- **Multi-Model AI Support**: GPT, Gemini, and Local LLM integration
- **Agentic AI Workflow**: Natural language query processing
- **Interactive Visualizations**: Plotly charts with AI-generated insights
- **Responsive Design**: Mobile-friendly interface
- **Production Ready**: Docker containerization and deployment

## 📋 Requirements

- Python 3.11+
- Docker (for containerized deployment)
- API Keys for OpenAI and/or Google Gemini

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-customer-analytics
   ```

2. **Install dependencies**
   ```bash
   make install
   # or
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   make run
   # or
   streamlit run app/main.py
   ```

### Docker Deployment

1. **Build the image**
   ```bash
   make build
   ```

2. **Deploy with Docker Compose**
   ```bash
   make deploy
   ```

3. **Access the application**
   - Local: http://localhost:8501
   - Network: http://your-server-ip:8501

## 🏗️ Project Structure

```
ai-customer-analytics/
├── app/                          # Main application package
│   ├── core/                     # Core business logic
│   │   ├── customer_data_loader.py
│   │   ├── narrative_generator.py
│   │   ├── visualization.py
│   │   ├── ai_provider.py
│   │   └── customer_ai_agent.py
│   ├── config/                   # Configuration management
│   │   ├── settings.py
│   │   └── production.py
│   ├── services/                 # Service layer
│   ├── utils/                    # Utility functions
│   ├── static/                   # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/                # HTML templates
│   ├── tests/                    # Test suite
│   │   ├── unit/
│   │   └── integration/
│   ├── data/                     # Data files
│   ├── notebooks/                # Jupyter notebooks
│   └── main.py                   # Streamlit application
├── docs/                         # Documentation
│   ├── api/
│   ├── deployment/
│   └── user_guide/
├── scripts/                      # Utility scripts
├── deployment/                   # Deployment configurations
├── Dockerfile                    # Docker configuration
├── docker-compose.yml           # Docker Compose setup
├── requirements.txt             # Python dependencies
├── Makefile                     # Development tasks
├── run.py                       # Application entry point
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `DEFAULT_AI_MODEL` | Default AI model | `gemini` |
| `SECRET_KEY` | Application secret key | Generated |
| `ENVIRONMENT` | Environment mode | `production` |
| `DEBUG` | Debug mode | `false` |

### AI Models

The application supports multiple AI models:

- **OpenAI GPT**: Advanced language model for text generation
- **Google Gemini**: Multimodal AI model for comprehensive analysis
- **Local LLM**: Template-based local processing

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test categories
pytest app/tests/unit/ -v
pytest app/tests/integration/ -v
```

## 📊 Usage

1. **Data Exploration**: Navigate to the "Data Exploration" page to view dataset statistics and insights
2. **AI Agent**: Use the "AI Agent" page to ask natural language questions about the data
3. **Visualizations**: Explore interactive charts and AI-generated insights
4. **Model Selection**: Choose between different AI models in the sidebar

## 🚀 Deployment

### Production Deployment

1. **Set up environment**
   ```bash
   cp env.example .env
   # Configure production settings
   ```

2. **Deploy with Docker**
   ```bash
   make deploy
   ```

3. **Monitor application**
   ```bash
   docker-compose logs -f ai-analytics-app
   ```

### Cloud Deployment

The application is ready for deployment on:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Heroku (with Docker)

## 🔍 Monitoring

- **Health Checks**: Built-in health check endpoint
- **Logging**: Structured logging with configurable levels
- **Metrics**: Application metrics and performance monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in `docs/`
- Review troubleshooting guide

## 🔄 Version History

- **v1.0.0**: Initial production release
  - Multi-model AI support
  - Agentic workflow implementation
  - Production-grade deployment
  - Responsive design
