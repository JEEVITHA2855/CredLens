# CredLens - AI-Powered Misinformation Detection

![CredLens Logo](docs/credlens-banner.png)

**Verify, Learn, Share Wisely**

CredLens is an AI-powered tool that detects potential misinformation in text or URL inputs and educates users with micro-lessons on identifying credible, trustworthy content.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Clone and navigate to the project**
   ```bash
   cd CredLens/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Build the dataset**
   ```bash
   cd ..
   python data/build_dataset.py
   ```

5. **Start the backend server**
   ```bash
   cd backend
   python run.py
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

The web app will open at `http://localhost:3000`

## 📋 Features

### Core Functionality
- **Claim Extraction**: Automatically extracts factual claims from text or URLs
- **Semantic Retrieval**: Uses FAISS and sentence transformers for similarity search
- **NLI Verification**: Employs RoBERTa-large-MNLI for evidence validation
- **Credibility Scoring**: Multi-factor credibility assessment

### Credibility Fingerprint
- **Source Credibility**: Domain-based trustworthiness scoring
- **Corroboration Count**: Number of independent supporting sources  
- **Language Risk**: Detection of sensational/emotional language
- **Overall Score**: Weighted combination of all factors

### Educational Features
- **Micro-lessons**: Contextual tips on claim verification
- **Suspicious Phrase Highlighting**: Visual identification of problematic language
- **Evidence Clustering**: Clear support vs. contradiction grouping
- **Verification Guides**: Step-by-step fact-checking instructions

### User Interface
- **Professional Design**: Clean, educational theme with Tailwind CSS
- **Responsive Layout**: Works on desktop and mobile devices
- **Interactive Elements**: Hover states, smooth animations
- **Accessibility**: WCAG compliant with proper focus management

## 🛠️ Technical Architecture

### Backend Stack
- **FastAPI**: Modern Python web framework
- **SQLite**: Lightweight database for caching and fact-checks
- **FAISS**: Vector similarity search
- **Sentence Transformers**: Text embeddings (all-MiniLM-L6-v2)
- **Transformers**: NLI model (facebook/bart-large-mnli)

### Frontend Stack
- **React 18**: Modern React with hooks
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client for API calls

### AI Components
- **Claim Extractor**: Pattern-based and sentence-scoring extraction
- **Semantic Retriever**: Embedding-based similarity search
- **NLI Verifier**: Natural language inference for evidence validation
- **Credibility Scorer**: Multi-dimensional credibility assessment
- **Micro-lesson Generator**: Context-aware educational content

## 📊 Dataset

The system includes a curated dataset with:
- **50+ Fact-checks** across multiple domains
- **Verified Sources** from reputable organizations
- **Demo Scenarios** for testing all verdict types
- **Diverse Topics**: Health, climate, technology, politics, science

### Dataset Categories
- Vaccines & Health
- Climate Change  
- Technology & 5G
- Elections & Politics
- Economics
- History
- Food & Agriculture
- Environment & Energy
- Science & Space
- Social Media

## 🧪 Demo Scenarios

Test the system with these prepared examples:

1. **True Claim**: "Vaccines are effective at preventing serious illness from COVID-19"
2. **False Claim**: "SHOCKING: Scientists REVEAL that 5G towers spread deadly coronavirus!"
3. **Mixed Evidence**: "Organic foods are much healthier than conventional foods"
4. **Unverified**: "A new study shows purple carrots improve memory by 50%"

## 📖 API Documentation

### Endpoints

#### `POST /analyze`
Analyze a claim or URL for misinformation.

**Request Body:**
```json
{
  "text": "Optional text claim",
  "url": "Optional URL to analyze"
}
```

**Response:**
```json
{
  "original_input": "Full input text",
  "extracted_claim": "Main factual claim",
  "verification_status": "Likely True|Mixed|Likely False|Unverified",
  "credibility_fingerprint": {
    "source_credibility": 0.75,
    "corroboration_count": 3,
    "language_risk": 0.2,
    "overall_score": 0.8
  },
  "evidence": [...],
  "suspicious_phrases": [...],
  "micro_lesson": {
    "tip": "Educational tip",
    "category": "source_verification"
  },
  "explanation": "Detailed explanation"
}
```

#### `GET /health`
Health check endpoint.

#### `GET /stats`
System statistics and model information.

## 🔧 Configuration

### Environment Variables
- `REACT_APP_API_URL`: Frontend API endpoint (default: http://localhost:8000)

### Model Configuration
Models are automatically downloaded on first run:
- Embedding model: `all-MiniLM-L6-v2`
- NLI model: `facebook/bart-large-mnli`

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing  
```bash
cd frontend
npm test
```

### Manual Testing
1. Start both servers
2. Visit `http://localhost:3000`
3. Try the demo scenarios
4. Test with custom claims and URLs

## 📝 Development

### Adding New Fact-checks
1. Edit `data/build_dataset.py`
2. Add new entries to `FACT_CHECKS`
3. Run the dataset builder
4. Restart the backend to rebuild the index

### Customizing the UI
- Colors and themes: `frontend/tailwind.config.js`
- Components: `frontend/src/components/`
- Styling: `frontend/src/index.css`

### Extending AI Components
- New verification methods: `backend/app/services/`
- Custom scoring logic: `backend/app/services/credibility_scorer.py`
- Educational content: `backend/app/services/micro_lesson_generator.py`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## ⚠️ Disclaimer

CredLens is an educational tool designed to help users develop media literacy skills. While it uses state-of-the-art AI techniques, it should not be the sole source for fact-checking. Always verify important information through multiple reliable sources.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation in the `docs/` folder
- Review the API documentation at `http://localhost:8000/docs`

---

**Built for the AI Hackathon - Empowering digital literacy through artificial intelligence** 🧠✨