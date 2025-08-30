# Streamlit Cloud Deployment Guide

## 🚀 Quick Deployment Steps

### 1. **Repository Setup**
- Ensure your repository is on GitHub
- Make sure `streamlit_app.py` is in the root directory
- Verify `requirements.txt` or `requirements-streamlit-cloud.txt` exists

### 2. **Streamlit Cloud Setup**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `streamlit_app.py`
6. Set requirements file: `requirements-streamlit-cloud.txt`

### 3. **Environment Variables**
Add these secrets in Streamlit Cloud:
```
OPENAI_API_KEY = your_openai_api_key
GEMINI_API_KEY = your_gemini_api_key
DEFAULT_AI_MODEL = gpt
```

## 🔧 Common Issues & Solutions

### **Issue 1: Module Import Errors**
**Error**: `ModuleNotFoundError: No module named 'core'`

**Solution**:
- Ensure `core/` directory is in the repository root
- Check that `__init__.py` files exist in all subdirectories
- Verify import paths in `streamlit_app.py`

### **Issue 2: Data File Not Found**
**Error**: `FileNotFoundError: data/customer_shopping_data.csv`

**Solution**:
- Ensure data file is in the repository
- Check file path in `streamlit_app.py`
- Verify file permissions

### **Issue 3: Memory Issues**
**Error**: `MemoryError` or slow loading

**Solution**:
- Use `requirements-streamlit-cloud.txt` for optimized dependencies
- Implement data caching with `@st.cache_data`
- Consider data sampling for large datasets

### **Issue 4: API Key Issues**
**Error**: `AuthenticationError` or `RateLimitError`

**Solution**:
- Verify API keys in Streamlit Cloud secrets
- Check API key permissions and quotas
- Use fallback local templates when APIs fail

## 📁 Required Files

### **Essential Files**:
```
├── streamlit_app.py              # Main Streamlit app (ONLY ONE)
├── requirements-streamlit-cloud.txt  # Optimized requirements
├── packages.txt                  # System dependencies
├── .streamlit/
│   ├── config.toml              # Streamlit configuration
│   └── secrets.toml             # Local secrets (not deployed)
├── core/                        # Core modules
│   ├── __init__.py
│   ├── data/
│   ├── ai/
│   └── visualization/
└── data/
    └── customer_shopping_data.csv
```

### **Optional Files**:
```
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore rules
└── docs/                        # Documentation
```

## 🔍 Debugging Tips

### **1. Check Logs**
- View deployment logs in Streamlit Cloud
- Look for import errors and missing dependencies
- Check for file path issues

### **2. Test Locally**
```bash
# Test with Streamlit Cloud requirements
pip install -r requirements-streamlit-cloud.txt
streamlit run streamlit_app.py
```

### **3. Verify Dependencies**
```bash
# Check if all imports work
python -c "import streamlit; import pandas; import plotly; print('All imports successful')"
```

### **4. Test Data Loading**
```bash
# Test data loading separately
python -c "import pandas as pd; df = pd.read_csv('data/customer_shopping_data.csv'); print(f'Loaded {len(df)} rows')"
```

## 🚨 Troubleshooting Checklist

- [ ] Repository is public or Streamlit Cloud has access
- [ ] `streamlit_app.py` is in the root directory
- [ ] Requirements file exists and is valid
- [ ] Data file is included in the repository
- [ ] All required modules are present
- [ ] API keys are set in Streamlit Cloud secrets
- [ ] No hardcoded paths in the code
- [ ] Error handling is implemented
- [ ] Memory usage is optimized

## 📞 Support

If you encounter issues:
1. Check the deployment logs
2. Verify all files are present
3. Test locally with the same requirements
4. Check Streamlit Cloud documentation
5. Review this troubleshooting guide

## 🔄 Deployment Workflow

1. **Local Testing**: Test with `requirements-streamlit-cloud.txt`
2. **Commit Changes**: Push to GitHub
3. **Deploy**: Streamlit Cloud will auto-deploy
4. **Verify**: Check the deployed app
5. **Debug**: If issues, check logs and this guide
