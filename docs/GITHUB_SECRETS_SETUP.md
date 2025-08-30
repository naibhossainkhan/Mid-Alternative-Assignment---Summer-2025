# 🔐 GitHub Secrets Setup Guide

This guide shows you how to securely manage API keys and other secrets using GitHub Secrets for different deployment scenarios.

## 📋 Table of Contents
- [GitHub Repository Secrets](#github-repository-secrets)
- [GitHub Actions Workflow](#github-actions-workflow)
- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
- [Local Development](#local-development)
- [Security Best Practices](#security-best-practices)

## 🏪 GitHub Repository Secrets

### How to Add Secrets to Your GitHub Repository:

1. **Go to your GitHub repository**
2. **Navigate to Settings → Secrets and variables → Actions**
3. **Click "New repository secret"**
4. **Add the following secrets:**

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-or-v1-...` |
| `GEMINI_API_KEY` | Your Google Gemini API key | `AIzaSy...` |
| `DEFAULT_AI_MODEL` | Default AI model to use | `gemini` |
| `SECRET_KEY` | Application secret key | `your-secret-key-here` |
| `ENVIRONMENT` | Deployment environment | `production` |

### Adding Secrets via GitHub CLI:
```bash
# Install GitHub CLI if you haven't already
# brew install gh (macOS)
# Then authenticate: gh auth login

# Add secrets
gh secret set OPENAI_API_KEY --body "your-openai-api-key"
gh secret set GEMINI_API_KEY --body "your-gemini-api-key"
gh secret set DEFAULT_AI_MODEL --body "gemini"
gh secret set SECRET_KEY --body "your-secret-key"
gh secret set ENVIRONMENT --body "production"
```

## 🤖 GitHub Actions Workflow

The `.github/workflows/deploy.yml` file shows how to use secrets in CI/CD:

```yaml
- name: Run tests
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
    DEFAULT_AI_MODEL: ${{ secrets.DEFAULT_AI_MODEL }}
  run: |
    python -m pytest tests/
```

## ☁️ Streamlit Cloud Deployment

### Option 1: Using Streamlit Secrets (Recommended)

1. **Create `.streamlit/secrets.toml` file:**
```toml
[ai_config]
openai_api_key = "your-openai-api-key-here"
gemini_api_key = "your-gemini-api-key-here"
default_model = "gemini"

[app_config]
secret_key = "your-secret-key-here"
environment = "production"
debug = false
```

2. **Deploy to Streamlit Cloud:**
   - Connect your GitHub repository
   - Streamlit Cloud will automatically read the secrets.toml file

### Option 2: Using Environment Variables in Streamlit Cloud

1. **In Streamlit Cloud dashboard:**
   - Go to your app settings
   - Add environment variables:
     - `OPENAI_API_KEY`
     - `GEMINI_API_KEY`
     - `DEFAULT_AI_MODEL`
     - `SECRET_KEY`

## 💻 Local Development

### Using .env file (Current Setup):
```bash
# Your .env file is already set up and working
cat .env
```

### Using Environment Variables:
```bash
# Set environment variables directly
export OPENAI_API_KEY="your-openai-api-key"
export GEMINI_API_KEY="your-gemini-api-key"
export DEFAULT_AI_MODEL="gemini"

# Run your app
streamlit run streamlit/streamlit_app_simple.py
```

## 🔒 Security Best Practices

### ✅ Do's:
- ✅ Use GitHub Secrets for production deployments
- ✅ Use .env files for local development
- ✅ Never commit secrets to Git
- ✅ Rotate API keys regularly
- ✅ Use different keys for different environments
- ✅ Limit API key permissions

### ❌ Don'ts:
- ❌ Never hardcode secrets in source code
- ❌ Never commit .env files to Git
- ❌ Never share API keys in public repositories
- ❌ Don't use the same keys for development and production
- ❌ Don't log or print API keys

## 🚀 Deployment Examples

### Heroku Deployment:
```bash
# Set Heroku config vars
heroku config:set OPENAI_API_KEY="your-openai-api-key"
heroku config:set GEMINI_API_KEY="your-gemini-api-key"
heroku config:set DEFAULT_AI_MODEL="gemini"
```

### Docker Deployment:
```dockerfile
# In your Dockerfile
ENV OPENAI_API_KEY=""
ENV GEMINI_API_KEY=""
ENV DEFAULT_AI_MODEL="gemini"

# Run with secrets
docker run -e OPENAI_API_KEY="your-key" -e GEMINI_API_KEY="your-key" your-app
```

### Kubernetes Deployment:
```yaml
# In your deployment.yaml
env:
- name: OPENAI_API_KEY
  valueFrom:
    secretKeyRef:
      name: ai-secrets
      key: openai-api-key
- name: GEMINI_API_KEY
  valueFrom:
    secretKeyRef:
      name: ai-secrets
      key: gemini-api-key
```

## 🔍 Testing Your Setup

### Test GitHub Secrets in Actions:
```yaml
- name: Test secrets
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
  run: |
    python -c "
    import os
    print('OpenAI Key:', '✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Missing')
    print('Gemini Key:', '✅ Set' if os.getenv('GEMINI_API_KEY') else '❌ Missing')
    "
```

### Test Local Environment:
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('OpenAI Key:', '✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Missing')
print('Gemini Key:', '✅ Set' if os.getenv('GEMINI_API_KEY') else '❌ Missing')
"
```

## 📞 Troubleshooting

### Common Issues:

1. **"ModuleNotFoundError: No module named 'config'"**
   - Solution: Check your Python path and import statements

2. **"Warning: OPENAI_API_KEY not found"**
   - Solution: Ensure your .env file exists and has the correct key names

3. **GitHub Actions failing with secret errors**
   - Solution: Check that secrets are properly set in GitHub repository settings

4. **Streamlit Cloud not reading secrets**
   - Solution: Ensure secrets.toml is in the correct location (.streamlit/secrets.toml)

## 🎯 Next Steps

1. **Set up GitHub Secrets** for your repository
2. **Test the GitHub Actions workflow**
3. **Deploy to Streamlit Cloud** using secrets
4. **Monitor your API usage** and costs
5. **Rotate your API keys** regularly

---

**Remember:** Security is an ongoing process. Regularly review and update your secrets management strategy!
