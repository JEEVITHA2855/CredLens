# 🔑 CredLens API Keys Setup Guide

## Required API Keys for Full Functionality

### 1. 🔍 Google Fact Check API
**Purpose:** Official fact-checking from verified sources like Snopes, PolitiFact, etc.

**How to get:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the "Fact Check Tools API"
   - Go to "APIs & Services" > "Library"
   - Search for "Fact Check Tools API"
   - Click "Enable"
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key

**Cost:** FREE (up to 1,000 queries/day)

### 2. 🌐 Bing Web Search API
**Purpose:** Search for recent news and authoritative sources

**How to get:**
1. Go to [Microsoft Azure Portal](https://portal.azure.com/)
2. Create a free Azure account if needed
3. Create a "Bing Search v7" resource:
   - Search for "Bing Search" in the marketplace
   - Select "Bing Search v7"
   - Choose Free pricing tier (F1) - 1,000 transactions/month
4. Get the API key:
   - Go to your created resource
   - Navigate to "Keys and Endpoint"
   - Copy one of the keys

**Cost:** FREE tier available (1,000 searches/month)

### 3. 📰 News API
**Purpose:** Access to news articles from major publishers

**How to get:**
1. Go to [NewsAPI.org](https://newsapi.org/)
2. Sign up for free account
3. Get your API key from the dashboard
4. Free tier: 1,000 requests/month

**Cost:** FREE tier (1,000 requests/month)

### 4. 🧠 OpenAI API (Optional - for enhanced AI reasoning)
**Purpose:** Advanced natural language processing for claim analysis

**How to get:**
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create account and add payment method
3. Generate API key in the API keys section

**Cost:** Pay-per-use (starts at ~$0.002/1K tokens)

## 📝 Environment Configuration

Create a `.env` file in your backend/demo directory with these keys:

```env
# Fact Checking APIs
GOOGLE_FACTCHECK_API_KEY=your_google_factcheck_api_key_here
BING_SEARCH_API_KEY=your_bing_search_api_key_here
NEWS_API_KEY=your_news_api_key_here

# Optional: Advanced AI
OPENAI_API_KEY=your_openai_api_key_here

# Model settings
MODEL_NAME=credlens-advanced
DEBUG=True
```

## 🚀 Quick Start Commands

After getting your API keys:

1. Update your .env file with real keys
2. Test the system:
   ```bash
   cd backend/demo
   python test_advanced.py
   ```

## 💰 Cost Breakdown (Monthly)

- **Google Fact Check API:** FREE (1,000 queries)
- **Bing Search API:** FREE (1,000 searches)  
- **News API:** FREE (1,000 requests)
- **Total for basic usage:** $0/month

For heavy usage:
- **Bing Search:** $5/1,000 additional searches
- **News API:** $449/month for unlimited
- **OpenAI:** ~$10-20/month for moderate usage

## 🔒 Security Best Practices

1. Never commit API keys to version control
2. Use environment variables only
3. Restrict API key permissions where possible
4. Monitor usage to prevent unexpected charges
5. Rotate keys regularly

## ✅ Testing Your Setup

Run this command to verify all APIs are working:
```bash
python test_api_connectivity.py
```

## 🆘 Troubleshooting

**Common Issues:**
- 401/403 errors: Check API key validity
- Rate limiting: Implement delays between requests  
- Quota exceeded: Monitor usage in API dashboards
- Network errors: Check internet connection and firewall

## 📞 Support

If you encounter issues:
1. Check API provider documentation
2. Verify API key permissions
3. Test with simple curl commands first
4. Contact API provider support if needed