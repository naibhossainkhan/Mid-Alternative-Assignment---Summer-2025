# 🤖 LangChain Deployment Guide for Streamlit Cloud

This guide shows you how to deploy the **full LangChain version** of your AI Analytics app to Streamlit Cloud.

## 📋 **Two App Versions Available**

### **1. Simple Version (No LangChain)**
- **File:** `streamlit/streamlit_app_simple.py`
- **Features:** Basic AI narrative generation, data visualization
- **Dependencies:** Minimal requirements

### **2. Full LangChain Version (Recommended)**
- **File:** `streamlit/streamlit_app.py`
- **Features:** AI agents, natural language queries, advanced AI workflows
- **Dependencies:** Includes LangChain ecosystem

## 🚀 **Deploying the LangChain Version**

### **Step 1: Choose Your App File**

When deploying to Streamlit Cloud, use:
```
Main file path: streamlit/streamlit_app.py
```

### **Step 2: Dependencies Are Ready**

The `requirements.txt` file now includes all LangChain dependencies:

```txt
# LangChain and AI Agents
langchain==0.0.350
langchain-openai==0.0.2
langchain-community==0.0.10
```

### **Step 3: Deploy to Streamlit Cloud**

1. **Go to [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in with GitHub**
3. **Click "New app"**
4. **Configure:**
   - **Repository:** `naibhossainkhan/Mid-Alternative-Assignment---Summer-2025`
   - **Branch:** `main`
   - **Main file path:** `streamlit/streamlit_app.py` ⭐
5. **Click "Deploy!"**

## 🔍 **LangChain Features Available**

### **AI Agent Capabilities:**
- ✅ **Natural Language Queries** - Ask questions in plain English
- ✅ **Intelligent Data Analysis** - AI agents understand your data
- ✅ **Automated Insights** - Generate insights automatically
- ✅ **Conversational Interface** - Chat with your data

### **Example Queries You Can Try:**
```
"What are the top 5 shopping malls by revenue?"
"Show me gender distribution of customers"
"Which age group spends the most money?"
"Compare revenue by payment method"
"Generate insights about customer behavior"
```

## 🔐 **Secrets Configuration**

Your secrets are already configured for both versions:

### **Local Development:**
```bash
# Uses .env file
OPENAI_API_KEY=your-openai-key
GEMINI_API_KEY=your-gemini-key
```

### **Streamlit Cloud:**
```toml
# Uses .streamlit/secrets.toml
[ai_config]
openai_api_key = "your-openai-key"
gemini_api_key = "your-gemini-key"
default_model = "gemini"
```

## 🧪 **Testing Locally**

### **Test LangChain Version:**
```bash
# Test LangChain dependencies
python -c "import sys; sys.path.append('src'); from customer_ai_agent import CustomerShoppingAgent; print('✅ LangChain works')"

# Run LangChain app locally
streamlit run streamlit/streamlit_app.py --server.port 8503
```

### **Test Simple Version:**
```bash
# Run simple app locally
streamlit run streamlit/streamlit_app_simple.py --server.port 8502
```

## 📊 **Feature Comparison**

| Feature | Simple Version | LangChain Version |
|---------|---------------|-------------------|
| Data Visualization | ✅ | ✅ |
| AI Narrative Generation | ✅ | ✅ |
| Natural Language Queries | ❌ | ✅ |
| AI Agents | ❌ | ✅ |
| Conversational Interface | ❌ | ✅ |
| Automated Insights | ❌ | ✅ |
| Dependencies | Minimal | Full LangChain |

## 🛠️ **Troubleshooting**

### **If LangChain Version Fails:**

1. **Check Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Use Minimal Version:**
   - Deploy `streamlit/streamlit_app_simple.py` instead
   - Use `requirements-streamlit.txt` for dependencies

3. **Check Streamlit Cloud Logs:**
   - Look for specific error messages
   - Verify all dependencies are installed

### **Common Issues:**

#### **"ModuleNotFoundError: langchain"**
**Solution:** Dependencies are already fixed in requirements.txt

#### **"ImportError: cannot import name"**
**Solution:** LangChain versions are compatible (0.0.350)

#### **"API Key not found"**
**Solution:** Check `.streamlit/secrets.toml` configuration

## 🎯 **Recommended Deployment**

### **For Production:**
Use the **LangChain version** (`streamlit/streamlit_app.py`) for:
- Full AI agent capabilities
- Natural language queries
- Advanced analytics features

### **For Testing:**
Use the **Simple version** (`streamlit/streamlit_app_simple.py`) for:
- Quick deployment
- Basic functionality
- Minimal dependencies

## 📈 **Performance Considerations**

### **LangChain Version:**
- **Pros:** Advanced AI features, natural language queries
- **Cons:** More dependencies, slightly slower startup
- **Best for:** Production use, advanced analytics

### **Simple Version:**
- **Pros:** Fast startup, minimal dependencies
- **Cons:** Limited AI features
- **Best for:** Testing, basic analytics

## 🚀 **Quick Deployment Commands**

```bash
# Deploy LangChain version
# Main file: streamlit/streamlit_app.py

# Deploy Simple version  
# Main file: streamlit/streamlit_app_simple.py
```

---

**🎉 You're ready to deploy the full LangChain version with advanced AI capabilities!**
