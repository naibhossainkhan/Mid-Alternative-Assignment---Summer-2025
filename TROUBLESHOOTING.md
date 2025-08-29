# Troubleshooting Guide

## Common Issues and Solutions

### 1. Timestamp Serialization Warning

**Issue:**
```
Serialization of dataframe to Arrow table was unsuccessful due to: 
("Could not convert Timestamp('2022-02-04 02:46:59.783424') with type Timestamp: 
tried to convert to int64", 'Conversion failed for column invoice_date with type object')
```

**Solution:**
- ✅ **Fixed**: Added `invoice_date_str` column for better Streamlit compatibility
- ✅ **Automatic**: Streamlit applies automatic fixes for Arrow compatibility
- ✅ **No Impact**: Warning doesn't affect functionality

**What was done:**
- Added string version of date column: `invoice_date_str`
- Updated data loader to handle datetime conversion properly
- Streamlit automatically handles the conversion

### 2. LangChain Import Errors

**Issue:**
```
ImportError: cannot import name 'RAW_SCHEMA_QUERY' from 'langchain_community.graphs.memgraph_graph'
```

**Solution:**
- ✅ **Simplified Version**: Use `streamlit_app_simple.py` (no LangChain required)
- ✅ **Full Version**: Install compatible LangChain versions
- ✅ **Demo Scripts**: Use `demo_agentic_workflow_simple.py`

**Commands:**
```bash
# Simplified version (recommended)
streamlit run streamlit_app_simple.py

# Full version (requires LangChain setup)
streamlit run streamlit_app.py
```

### 3. Missing Dependencies

**Issue:**
```
ModuleNotFoundError: No module named 'openai'
```

**Solution:**
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install specific packages
pip install streamlit pandas plotly openai google-generativeai
```

### 4. Data File Not Found

**Issue:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/customer_shopping_data.csv'
```

**Solution:**
- Ensure `data/customer_shopping_data.csv` exists in the project directory
- Check file permissions
- Verify the file path is correct

### 5. API Key Issues

**Issue:**
```
Error: API key not found
```

**Solution:**
- **Local Model**: Works without API keys (default)
- **Gemini**: Your API key is pre-configured
- **OpenAI**: Set `export OPENAI_API_KEY="your_key"`

### 6. Memory Issues

**Issue:**
```
MemoryError or slow performance
```

**Solution:**
- Dataset is ~7.2MB, ensure sufficient RAM
- Use simplified demo scripts for testing
- Close other applications if needed

### 7. Text Readability Issues

**Issue:**
```
AI-Generated Dashboard Insights text is not readable
```

**Solution:**
- ✅ **Fixed**: Updated CSS styling for better contrast
- ✅ **Background**: Changed to light gray (#f0f2f6)
- ✅ **Text Color**: Set to dark gray (#262730)
- ✅ **Font Size**: Increased to 1rem with proper line height

**What was done:**
- Enhanced `.ai-insight` CSS class with better colors
- Improved `.query-result` styling for code blocks
- Added proper contrast ratios for accessibility

### 8. Example Query Buttons Not Working

**Issue:**
```
When clicking example query buttons, the text doesn't appear in the query input field
```

**Solution:**
- ✅ **Fixed**: Added proper session state management
- ✅ **Query Input**: Now uses `value=st.session_state.query`
- ✅ **Button Layout**: Improved to 3-column layout with tooltips
- ✅ **Clear Button**: Added clear functionality

**What was done:**
- Initialize session state for query field
- Update text input to use session state value
- Improve button layout and add tooltips
- Add clear query functionality

### 9. AI Model Selection

**Feature:**
```
Model selection dropdown in sidebar with Local LLM, Gemini, and GPT options
```

**How to use:**
- **Sidebar**: Look for "🤖 AI Model Selection" in the left sidebar
- **Local LLM**: ✅ Ready to use (no API key required)
- **Gemini**: 🔮 Your API key is pre-configured
- **GPT**: ⚡ Requires OpenAI API key setup

**What was added:**
- Model selection dropdown in sidebar
- Real-time model switching
- Status indicators for each model
- Automatic fallback to Local LLM if API models fail
- Current model display in AI Agent page

### 10. Session State Initialization Error

**Issue:**
```
KeyError: 'st.session_state has no key "selected_model". Did you forget to initialize it?
```

**Solution:**
- ✅ **Fixed**: Moved session state initialization to beginning of main function
- ✅ **Proper Order**: Initialize before using session state variables
- ✅ **No Duplicates**: Removed duplicate initialization code

**What was done:**
- Initialize `selected_model` and `query` at the start of main function
- Remove duplicate initialization from sidebar and AI Agent sections
- Ensure session state is available before any component tries to use it

## Performance Tips

### 1. Fast Startup
```bash
# Use simplified version for quick demos
python demo_agentic_workflow_simple.py
```

### 2. Web Interface
```bash
# Access Streamlit app
streamlit run streamlit_app_simple.py
# Then open: http://localhost:8501
```

### 3. Command Line Demos
```bash
# Multi-model AI demo
python demo_multi_model_simple.py

# Agentic workflow demo
python demo_agentic_workflow_simple.py

# Textual summary demo
python demo_textual_summary_simple.py
```

## System Requirements

### Minimum Requirements
- **Python**: 3.8+
- **RAM**: 4GB+
- **Storage**: 100MB free space
- **Internet**: For API calls (optional)

### Recommended
- **Python**: 3.11+
- **RAM**: 8GB+
- **Storage**: 500MB free space
- **Internet**: Stable connection for AI APIs

## Getting Help

### 1. Test Installation
```bash
python test_installation.py
```

### 2. Check Dependencies
```bash
pip list | grep -E "(streamlit|pandas|plotly|openai)"
```

### 3. Verify Data
```bash
ls -la data/customer_shopping_data.csv
```

### 4. Run Simple Demo
```bash
python customer_demo_simple.py
```

## Success Indicators

✅ **App Running**: Streamlit shows "You can now view your Streamlit app"
✅ **Data Loaded**: "Successfully loaded 99,457 records"
✅ **AI Working**: Local model generates insights
✅ **Visualizations**: Charts display correctly
✅ **Queries Work**: Natural language processing functions

## Contact

If you encounter issues not covered here:
1. Check the README.md for detailed instructions
2. Run the test script: `python test_installation.py`
3. Try the simplified demos first
4. Ensure all dependencies are installed
