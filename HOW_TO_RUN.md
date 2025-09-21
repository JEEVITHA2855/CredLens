# How to Run CredLens with OpenAI Integration

## 🚀 Quick Start Guide

### Step 1: Fix Your OpenAI API Key

Your current API key has exceeded its quota. Here's how to fix it:

#### Option A: Add Credits to Existing Key
1. Go to [OpenAI Billing](https://platform.openai.com/account/billing)
2. Add a payment method
3. Purchase credits ($5 minimum recommended)
4. Your existing key will work once credits are added

#### Option B: Create New API Key
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Click "Create new secret key"
3. Copy the new key (starts with `sk-`)
4. Replace in your `.env` file

### Step 2: Update Your Environment File

Navigate to your demo folder and update the API key:

```bash
# Edit the .env file
cd e:\CredLens\backend\demo
notepad .env
```

Replace the OpenAI key line:
```
OPENAI_API_KEY=your_new_working_key_here
```

### Step 3: Test OpenAI Integration

```bash
# Test the setup (no API calls)
python backend/demo/test_openai_setup.py

# Test with real OpenAI API calls
python backend/demo/test_openai.py

# Run full system demo
python backend/demo/credlens_demo.py
```

## 🏃 Running Different Components

### 1. Backend API Server

```bash
cd e:\CredLens
python backend/app.py
```
Server runs at: `http://localhost:5000`

### 2. Frontend React App

```bash
cd e:\CredLens\frontend
npm install
npm start
```
App runs at: `http://localhost:3000`

### 3. OpenAI Demo (New!)

```bash
cd e:\CredLens
python backend/demo/test_openai.py
```

## 🧪 Testing Your Setup

### Quick Test
```bash
python backend/demo/test_openai_setup.py
```

### Interactive Testing
```bash
python backend/demo/test_openai.py
# Choose option 3 for interactive mode
```

### Full Demo
```bash
python backend/demo/credlens_demo.py
```

## 🔑 Getting Additional API Keys (Optional)

### Google Fact Check API (FREE)
1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create project → Enable "Fact Check Tools API"
3. Create API Key → Add to `.env`:
```
GOOGLE_FACTCHECK_API_KEY=your_google_key
```

### News API (FREE Tier)
1. Go to [NewsAPI.org](https://newsapi.org/register)
2. Register → Get API key → Add to `.env`:
```
NEWS_API_KEY=your_news_api_key
```

## 📱 Using the System

### Web Interface
1. Start backend: `python backend/app.py`
2. Start frontend: `cd frontend && npm start`
3. Open: `http://localhost:3000`
4. Enter claims and get AI-powered analysis!

### Command Line Testing
```bash
# Test specific claims
python backend/demo/test_openai.py

# Interactive mode for custom testing
python backend/demo/test_openai.py
# Then choose option 3
```

## 🎯 Integration Examples

### Using OpenAI Detector in Your Code

```python
from backend.demo.openai_detector import OpenAIDetector

# Initialize
detector = OpenAIDetector()

# Test connection
connection = detector.test_connection()
print(f"Status: {connection['status']}")

# Analyze a claim
result = detector.analyze_claim("The Earth is flat")
print(f"Verdict: {result['verdict']}")
print(f"Confidence: {result['confidence']}%")
print(f"Explanation: {result['explanation']}")
```

## 🚨 Troubleshooting

### OpenAI API Issues
- **Quota exceeded**: Add billing/credits at platform.openai.com
- **Invalid key**: Create new key at platform.openai.com/api-keys
- **Model not found**: Check `.env` has `MODEL_NAME=gpt-3.5-turbo`

### Environment Issues
```bash
# Reinstall packages if needed
pip install openai==0.28.1 python-dotenv

# Check your environment
python backend/demo/test_openai_setup.py
```

### Frontend Issues
```bash
cd frontend
npm install
npm start
```

## 📊 What You Get

With working API keys, CredLens provides:
- 🤖 **AI-Powered Analysis**: Advanced reasoning with GPT-3.5-turbo
- 🔬 **Scientific Validation**: Local fact database verification
- 📰 **Multi-Source Checking**: News and fact-check API integration
- 📊 **Confidence Scoring**: Reliability percentages for each verdict
- 🎯 **Detailed Explanations**: Why claims are true/false/ambiguous

## 🎉 Success!

Once your OpenAI key is working, you'll see:
```
✅ OpenAI API Connection: SUCCESS
🤖 AI Analysis: Ready for misinformation detection!
```

Your CredLens system is now enterprise-ready with advanced AI capabilities! 🚀