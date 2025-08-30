# 🛠️ Streamlit Cloud Deployment Troubleshooting

This guide helps you resolve common deployment issues on Streamlit Cloud.

## ❌ **Common Error: "installer returned a non-zero exit code"**

### **Problem:**
```
[07:35:13] ❗️ installer returned a non-zero exit code
[07:35:13] ❗️ Error during processing dependencies! Please fix the error and push an update, or try restarting the app.
```

### **Solutions:**

#### **Solution 1: Use Fixed Version Requirements**

The main `requirements.txt` file has been updated with fixed versions to avoid conflicts:

```txt
# Core Streamlit Framework
streamlit==1.32.0

# Data Processing and Analysis
pandas==2.1.4
numpy==1.24.3
scikit-learn==1.3.2
scipy==1.11.4

# Data Visualization
plotly==5.17.0
matplotlib==3.8.2
seaborn==0.13.0

# AI and Machine Learning
openai==1.6.1
google-generativeai==0.3.2
langchain==0.1.0
langchain-openai==0.0.5
tiktoken==0.5.2

# Environment and Configuration
python-dotenv==1.0.0

# Additional dependencies for Streamlit Cloud compatibility
markdown-it-py==4.0.0
mdurl==0.1.2
pygments==2.19.2
rich==14.1.0

# Production and Deployment
gunicorn==21.2.0
```

#### **Solution 2: Use Minimal Requirements (Alternative)**

If the main requirements still cause issues, use the minimal `requirements-streamlit.txt`:

```txt
# Minimal requirements for Streamlit Cloud deployment
streamlit==1.32.0
pandas==2.1.4
numpy==1.24.3
plotly==5.17.0
matplotlib==3.8.2
seaborn==0.13.0
openai==1.6.1
google-generativeai==0.3.2
tiktoken==0.5.2
python-dotenv==1.0.0
markdown-it-py==4.0.0
mdurl==0.1.2
pygments==2.19.2
rich==14.1.0
```

## 🔧 **Step-by-Step Fix**

### **Step 1: Update Your Repository**

```bash
# Commit the updated requirements
git add requirements.txt requirements-streamlit.txt .streamlit/config.toml
git commit -m "Fix Streamlit Cloud deployment dependencies"
git push origin main
```

### **Step 2: Redeploy on Streamlit Cloud**

1. **Go to your Streamlit Cloud dashboard**
2. **Click "Redeploy" or "Deploy"**
3. **Wait for the build to complete**

### **Step 3: If Still Failing, Try Alternative Approach**

If the main `requirements.txt` still fails:

1. **Rename the minimal requirements file:**
   ```bash
   mv requirements-streamlit.txt requirements.txt
   ```

2. **Commit and push:**
   ```bash
   git add requirements.txt
   git commit -m "Use minimal requirements for Streamlit Cloud"
   git push origin main
   ```

3. **Redeploy on Streamlit Cloud**

## 🔍 **Other Common Issues**

### **Issue 1: Import Errors**

**Error:** `ModuleNotFoundError: No module named 'config'`

**Solution:** The import paths are already fixed in your code.

### **Issue 2: Memory Issues**

**Error:** `MemoryError` or app crashes

**Solution:**
- Use the minimal requirements file
- Reduce data processing in the app
- Add memory optimization to your code

### **Issue 3: Timeout Issues**

**Error:** App takes too long to load

**Solution:**
- Optimize data loading
- Add caching to your Streamlit app
- Use smaller datasets for initial testing

## 🧪 **Testing Your Fix**

### **Test 1: Local Testing**
```bash
# Test with the new requirements locally
pip install -r requirements.txt
streamlit run streamlit/streamlit_app_simple.py
```

### **Test 2: Check Dependencies**
```bash
# Verify all dependencies can be installed
pip install -r requirements.txt --dry-run
```

### **Test 3: Streamlit Cloud Logs**
1. **Check the deployment logs** in Streamlit Cloud dashboard
2. **Look for specific error messages**
3. **Verify the build process completes**

## 📋 **Deployment Checklist**

Before deploying, ensure:

- [ ] `requirements.txt` has fixed versions (not ranges)
- [ ] All dependencies are compatible
- [ ] No development-only packages included
- [ ] `.streamlit/config.toml` is configured
- [ ] `.streamlit/secrets.toml` exists locally
- [ ] Code runs locally without errors

## 🚀 **Quick Fix Commands**

```bash
# Update requirements and redeploy
git add requirements.txt
git commit -m "Fix deployment dependencies"
git push origin main

# Then redeploy on Streamlit Cloud
```

## 📞 **If All Else Fails**

1. **Check Streamlit Cloud status** at [status.streamlit.io](https://status.streamlit.io)
2. **Try deploying a minimal test app** first
3. **Contact Streamlit support** if the issue persists
4. **Use alternative deployment platforms** like Heroku or Railway

---

**💡 Pro Tip:** Always test your app locally with the exact same requirements before deploying to Streamlit Cloud!
