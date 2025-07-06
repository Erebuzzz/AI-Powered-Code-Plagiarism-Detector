# 🚀 AI-Powered Code Plagiarism Detector

A comprehensive, modern web application that uses advanced AI models to detect code plagiarism and similarity with detailed analysis and insights.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![Next.js](https://img.shields.io/badge/Next.js-15.3.5-black)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![Vercel](https://img.shields.io/badge/Vercel-Ready-black)
![Render](https://img.shields.io/badge/Render-Ready-blue)

## ✨ Features

### 🔍 **Advanced Code Analysis**
- **Multi-language support**: Python, JavaScript, TypeScript, Java, C++, C#, PHP, Ruby, Go, Rust, Swift, Kotlin
- **AI-powered detection**: Uses state-of-the-art models like CodeBERT, UniXcoder, and CodeT5
- **Semantic similarity**: Deep understanding of code structure and logic
- **Real-time analysis**: Fast processing with cached models

### 📊 **Comprehensive Reporting**
- **Detailed metrics**: Lines of code, complexity, quality scores
- **Visual similarity scores**: Color-coded risk levels and progress bars
- **Code structure analysis**: Control flow, functions, imports, variables
- **Quality assessment**: Readability, maintainability, code smells, best practices
- **Pattern detection**: Algorithm patterns, data structures, design patterns

### 🎨 **Modern UI/UX**
- **Dark/Light mode**: Toggle between themes
- **Responsive design**: Works on desktop, tablet, and mobile
- **Interactive code editor**: Monaco editor with syntax highlighting
- **Drag & drop uploads**: Easy file uploads with format detection
- **Real-time feedback**: Live analysis results and error handling

### 🔧 **Enhanced Features**
- **Batch analysis**: Compare multiple files at once
- **Enhanced AI mode**: Optional Cohere integration for advanced analysis
- **Code comparison**: Side-by-side similarity analysis
- **Export functionality**: Download results in various formats
- **API integration**: RESTful API for programmatic access

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and Python 3.11+
- API keys (optional but recommended):
  - [Cohere API Key](https://cohere.ai/) (for enhanced analysis)
  - [Hugging Face API Key](https://huggingface.co/settings/tokens) (for additional models)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AI-Powered-Code-Plagiarism-Detector.git
   cd AI-Powered-Code-Plagiarism-Detector
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (optional but recommended)
   ```

3. **Start the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

4. **Start the frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## 🌐 Production Deployment

Deploy to the cloud using Vercel (frontend) and Render (backend):
- See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
- Support for automatic deployments from Git

## 🛠️ Development Setup

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
├── backend/                 # Flask API server
│   ├── routes/             # API route handlers
│   ├── services/           # Business logic services
│   ├── utils/              # Utility functions
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js React application
│   ├── src/app/           # App router pages and components
│   ├── components/        # Reusable React components
│   ├── contexts/          # React context providers
│   └── package.json       # Node.js dependencies
├── render.yaml           # Render deployment config
├── prepare-deployment.*  # Deployment preparation scripts
└── DEPLOYMENT.md         # Detailed deployment guide
```

## 🔌 API Endpoints

### Core Analysis
- `POST /api/analyze` - Basic code analysis
- `POST /api/analyze-enhanced` - Enhanced AI analysis
- `POST /api/compare` - Compare two code snippets
- `POST /api/batch-analyze` - Analyze multiple files

### Utility
- `GET /health` - Health check endpoint
- `GET /api/supported-languages` - List supported languages

### Example API Usage
```javascript
const response = await fetch('/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: 'def hello_world():\n    print("Hello, World!")',
    language: 'python',
    checkDatabase: true
  })
});
```

## 🧠 AI Models Used

### Code Understanding
- **CodeBERT**: Microsoft's pre-trained model for code understanding
- **UniXcoder**: Enhanced code representation model
- **CodeT5**: Text-to-code generation and understanding
- **GraphCodeBERT**: Graph-neural-network-based code model

### Similarity Detection
- **Sentence Transformers**: For semantic similarity
- **TF-IDF**: Traditional text similarity
- **AST Analysis**: Abstract syntax tree comparison
- **Custom Embeddings**: Domain-specific code embeddings

## 🔧 Configuration

### Environment Variables
```bash
# API Keys (optional but recommended)
COHERE_API_KEY=your_cohere_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key

# Backend Configuration
FLASK_ENV=production
CORS_ORIGINS=https://yourdomain.com
SECRET_KEY=your_secure_secret_key

# Frontend Configuration
NEXT_PUBLIC_BACKEND_URL=https://api.yourdomain.com
```

### Supported File Types
- Python: `.py`
- JavaScript: `.js`, `.jsx`
- TypeScript: `.ts`, `.tsx`
- Java: `.java`
- C++: `.cpp`, `.cc`, `.cxx`
- C: `.c`
- C#: `.cs`
- PHP: `.php`
- Ruby: `.rb`
- Go: `.go`
- Rust: `.rs`
- Swift: `.swift`
- Kotlin: `.kt`

## 🚢 Deployment

### Vercel + Render (Recommended)
- **Frontend**: Deploy to Vercel
- **Backend**: Deploy to Render

### Cloud Platforms
- **AWS ECS/Fargate**: Container orchestration
- **Google Cloud Run**: Serverless containers
- **Heroku**: Platform-as-a-Service
- **DigitalOcean Apps**: Simple container deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📊 Performance & Scalability

### Performance Metrics
- **Analysis Speed**: ~2-5 seconds per file
- **Concurrent Users**: Supports 100+ concurrent analyses
- **File Size Limit**: 10MB per file
- **Memory Usage**: ~2GB for full model cache

### Optimization Features
- **Model Caching**: Pre-loaded models for faster inference
- **Result Caching**: Cache analysis results for identical code
- **Background Processing**: Queue system for large batch jobs
- **CDN Ready**: Static assets optimized for CDN delivery

## 🔐 Security Features

- **Input Validation**: Comprehensive file and code validation
- **Rate Limiting**: API rate limiting to prevent abuse
- **CORS Protection**: Configurable cross-origin policies
- **Secure Headers**: Security headers via Nginx
- **Environment Isolation**: Containerized execution environment

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
python test_api.py  # Integration tests
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:e2e  # End-to-end tests
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript/TypeScript
- Write tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face**: For providing state-of-the-art NLP models
- **Microsoft**: For CodeBERT and related research
- **Cohere**: For advanced language model capabilities
- **Next.js Team**: For the excellent React framework
- **Flask Community**: For the lightweight Python web framework

## 📞 Support

- **Documentation**: Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join GitHub Discussions for questions
- **Email**: support@yourdomain.com

## 🚀 Roadmap

### Upcoming Features
- [ ] **Database Integration**: PostgreSQL for persistent storage
- [ ] **User Authentication**: Multi-user support with accounts
- [ ] **Version Control Integration**: Git repository analysis
- [ ] **Advanced Reporting**: PDF/HTML report generation
- [ ] **API Rate Plans**: Different API access levels
- [ ] **Mobile App**: React Native mobile application
- [ ] **VS Code Extension**: IDE integration
- [ ] **Webhook Support**: Real-time notifications

### Performance Improvements
- [ ] **Distributed Computing**: Multi-node analysis
- [ ] **GPU Acceleration**: CUDA support for faster inference
- [ ] **Advanced Caching**: Redis-based result caching
- [ ] **CDN Integration**: Global content delivery

---

<div align="center">
  <strong>🚀 Star this repository if you find it useful! 🚀</strong>
</div>
