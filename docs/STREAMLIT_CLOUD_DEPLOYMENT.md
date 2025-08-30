# ☁️ Streamlit Cloud Deployment Guide

This guide will help you deploy your AI Analytics application to Streamlit Cloud while keeping your secrets secure.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
- [Secrets Management](#secrets-management)
- [Troubleshooting](#troubleshooting)

## ✅ Prerequisites

Before deploying, ensure you have:

- ✅ GitHub repository with your code
- ✅ OpenAI API key (optional)
- ✅ Google Gemini API key (optional)
- ✅ Streamlit Cloud account (free)

## 💻 Local Development Setup

### Current Setup (Already Working)

Your local development is already configured with:

1. **`.env` file** - Contains your API keys for local development
2. **`.streamlit/secrets.toml`** - Contains your API keys for Streamlit Cloud
3. **Updated `config.py`** - Supports multiple secret sources

### Test Local Development

```bash
# Test that everything works locally
python test_streamlit_secrets.py

# Run the app locally
streamlit run streamlit/streamlit_app_simple.py --server.port 8502
```

## ☁️ Streamlit Cloud Deployment

### Step 1: Prepare Your Repository

Your repository is already properly configured:

- ✅ `.streamlit/secrets.toml` - Contains your API keys
- ✅ `.gitignore` - Excludes secrets from Git
- ✅ `config.py` - Supports Streamlit secrets
- ✅ `requirements.txt` - Lists dependencies

### Step 2: Deploy to Streamlit Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Configure your app:**

```
Repository: your-username/your-repo-name
Branch: main
Main file path: streamlit/streamlit_app_simple.py
```

5. **Click "Deploy!"**

### Step 3: Verify Deployment

After deployment, your app will be available at:
`https://your-app-name-your-username.streamlit.app`

## 🔐 Secrets Management

### How Secrets Work

Your application uses a **priority-based secret loading system**:

1. **Environment Variables** (highest priority)
2. **Streamlit Secrets** (for Streamlit Cloud)
3. **.env file** (for local development)

### Current Secret Configuration

#### Local Development (`.env`):
```bash
OPENAI_API_KEY=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
GEMINI_API_KEY=AIzaSyCSgthqUPp1X--3dAu7bihS_00izLY8PlY
DEFAULT_AI_MODEL=gemini
```

#### Streamlit Cloud (`.streamlit/secrets.toml`):
```toml
[ai_config]
openai_api_key = "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"
gemini_api_key = "AIzaSyCSgthqUPp1X--3dAu7bihS_00izLY8PlY"
default_model = "gemini"
```

### Security Features

- ✅ **Secrets are NOT in Git** - `.streamlit/secrets.toml` is ignored
- ✅ **Local development works** - Uses `.env` file
- ✅ **Streamlit Cloud works** - Uses `.streamlit/secrets.toml`
- ✅ **Fallback mechanisms** - Graceful handling of missing secrets

## 🚀 Deployment Checklist

Before deploying, verify:

- [ ] Repository is pushed to GitHub
- [ ] `.streamlit/secrets.toml` exists with your API keys
- [ ] `.gitignore` excludes `.streamlit/secrets.toml`
- [ ] `requirements.txt` includes all dependencies
- [ ] Local app runs successfully
- [ ] `test_streamlit_secrets.py` passes all tests

## 🔍 Testing Your Deployment

### Test 1: Local Development
```bash
python test_streamlit_secrets.py
streamlit run streamlit/streamlit_app_simple.py
```

### Test 2: Streamlit Cloud
1. Deploy to Streamlit Cloud
2. Check the app loads without errors
3. Test AI functionality (narrative generation, etc.)

### Test 3: Secret Loading
Your app should automatically detect and use the correct secret source:
- **Local**: Uses `.env` file
- **Streamlit Cloud**: Uses `.streamlit/secrets.toml`

## 🛠️ Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'config'"
**Solution**: The import paths are already fixed in your code.

#### 2. "Warning: OPENAI_API_KEY not found"
**Solution**: Check that `.streamlit/secrets.toml` exists and has correct keys.

#### 3. "Streamlit app not loading"
**Solution**: 
- Check the main file path in Streamlit Cloud settings
- Ensure `streamlit/streamlit_app_simple.py` exists
- Check the Streamlit Cloud logs for errors

#### 4. "AI features not working"
**Solution**:
- Verify API keys are correct in `.streamlit/secrets.toml`
- Check that the AI models are enabled in your config
- Test with the local version first

### Debug Commands

```bash
# Test configuration loading
python test_streamlit_secrets.py

# Test Streamlit app locally
streamlit run streamlit/streamlit_app_simple.py --server.port 8502

# Check if secrets are loaded
python -c "from config import config; print('OpenAI:', config.is_model_available('gpt')); print('Gemini:', config.is_model_available('gemini'))"
```

## 📊 Monitoring Your Deployment

### Streamlit Cloud Dashboard
- Monitor app performance
- Check deployment logs
- View usage statistics

### API Usage Monitoring
- Monitor OpenAI API usage and costs
- Monitor Google Gemini API usage
- Set up alerts for high usage

## 🔄 Updating Your Deployment

### Code Updates
1. Make changes to your code
2. Push to GitHub
3. Streamlit Cloud automatically redeploys

### Secret Updates
1. Update `.streamlit/secrets.toml` locally
2. Push to GitHub (secrets file is ignored)
3. Redeploy in Streamlit Cloud dashboard

## 🎯 Next Steps

1. **Deploy to Streamlit Cloud** using the steps above
2. **Test all functionality** in the deployed app
3. **Share your app** with others
4. **Monitor usage** and costs
5. **Set up custom domain** (optional)

## 📞 Support

If you encounter issues:

1. **Check Streamlit Cloud logs** in the dashboard
2. **Run local tests** to isolate issues
3. **Review this guide** for common solutions
4. **Check Streamlit documentation** for platform-specific issues

---

**🎉 Congratulations!** Your AI Analytics app is now ready for secure deployment on Streamlit Cloud!
