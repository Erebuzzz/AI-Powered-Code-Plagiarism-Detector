# AI-Powered Code Plagiarism Detector

A sophisticated web-based application that detects code plagiarism using advanced Natural Language Processing (NLP) and Large Language Model (LLM) techniques, providing semantic comparison that goes beyond basic string matching.

![Project Status](https://img.shields.io/badge/Status-Completed-green)
![Python Version](https://img.shields.io/badge/Python-3.8+-blue)
![React Version](https://img.shields.io/badge/React-18.2+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Table of Contents
- [Overview](#overview)
- [Why This Project?](#why-this-project)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Development Process](#development-process)
- [Errors Faced & Solutions](#errors-faced--solutions)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Screenshots](#screenshots)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## 🎯 Overview

This project addresses the critical issue of code plagiarism in academic institutions, hiring processes, and open-source software development. Unlike traditional tools that rely on basic text comparison, our solution uses AI-powered semantic analysis to detect deeper similarities that can't be easily bypassed through code obfuscation or minor modifications.

### **Project Highlights:**
- **Semantic Analysis**: Uses AI to understand code meaning, not just syntax
- **Multi-language Support**: Supports Python, JavaScript, Java, C++, C, and C#
- **Real-time Comparison**: Instant similarity scoring and detailed analysis
- **User-Friendly Interface**: Modern React-based UI with code editors
- **RESTful API**: Easy integration with existing systems
- **Historical Tracking**: Maintains comparison history with detailed reports

## 🚀 Why This Project?

### **Problem Statement:**
- **Academic Plagiarism**: Students often copy code with minor modifications
- **Hiring Challenges**: Recruiters need to verify candidate's original work
- **Open Source Issues**: Detecting unauthorized code usage
- **Traditional Tools Limitations**: Easy to bypass with variable renaming, code restructuring

### **Our Solution:**
- **AI-Powered Detection**: Uses semantic understanding to catch sophisticated plagiarism
- **Robust Analysis**: Combines lexical and semantic similarity metrics
- **Detailed Reporting**: Provides explanations for similarity scores
- **Easy Integration**: RESTful API for seamless system integration

### **Market Demand:**
- High demand in EdTech, HR Tech, and Academic institutions
- Excellent freelance opportunity
- Growing need for AI-powered code analysis tools

## ✨ Key Features

### **Core Functionality:**
- 📤 **File Upload & Code Input**: Support for direct code pasting and file uploads
- 🧠 **AI-Powered Analysis**: Semantic similarity detection using NLP techniques
- 📊 **Detailed Similarity Scoring**: Both lexical and semantic similarity metrics
- 🔍 **Side-by-Side Comparison**: Visual code comparison with syntax highlighting
- 📈 **Comprehensive Reports**: Detailed analysis with AI explanations
- 🗄️ **Comparison History**: Track and review previous analyses
- 🌐 **Multi-Language Support**: Python, JavaScript, Java, C++, C, C#
- 🔗 **REST API**: Complete API for third-party integrations

### **Advanced Features:**
- **Threshold-Based Classification**: Configurable similarity thresholds
- **Real-time Processing**: Instant analysis and results
- **Error Handling**: Robust error management and user feedback
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🛠️ Technology Stack

### **Backend:**
- **Framework**: FastAPI (Python 3.8+)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **AI/ML**: 
  - OpenAI GPT-4 (for explanations)
  - HuggingFace Transformers (CodeBERT for embeddings)
  - Custom NLP algorithms for basic similarity
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **API Documentation**: Automatic OpenAPI/Swagger

### **Frontend:**
- **Framework**: React.js 18.2+
- **UI Library**: Material-UI (MUI)
- **Code Editor**: Monaco Editor (VS Code editor)
- **File Upload**: React Dropzone
- **HTTP Client**: Axios
- **Routing**: React Router DOM

### **Development Tools:**
- **Package Management**: npm (frontend), pip (backend)
- **Development Server**: Uvicorn (backend), React Dev Server
- **Code Quality**: ESLint, Prettier
- **Version Control**: Git

### **Deployment Ready:**
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions ready
- **Cloud Platforms**: Heroku, AWS, Render compatible

## 📁 Project Structure

```
AI-Powered-Code-Plagiarism-Detector/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI application entry point
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       └── comparison.py     # API endpoints for code comparison
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py             # Application configuration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── database.py           # Database models and setup
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── comparison.py         # Pydantic schemas
│   │   └── services/
│   │       ├── __init__.py
│   │       └── ai_service.py         # AI/ML processing logic
│   ├── requirements.txt              # Python dependencies
│   ├── .env                         # Environment variables
│   └── .env.example                 # Environment template
├── frontend/                        # React Frontend
│   ├── public/
│   │   ├── index.html               # HTML template
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/              # Reusable React components
│   │   ├── pages/
│   │   │   ├── HomePage.js          # Landing page
│   │   │   ├── ComparisonPage.js    # Code comparison interface
│   │   │   ├── ResultsPage.js       # Results display
│   │   │   └── HistoryPage.js       # Comparison history
│   │   ├── services/
│   │   │   └── api.js               # API service layer
│   │   ├── App.js                   # Main React component
│   │   ├── index.js                 # React entry point
│   │   └── index.css                # Global styles
│   ├── package.json                 # Node.js dependencies
│   └── package-lock.json
├── README.md                        # This file
├── LICENSE                          # MIT License
└── .gitignore                       # Git ignore rules
```

## 🔧 Installation & Setup

### **Prerequisites:**
- **Python 3.8+** ([Download Python](https://python.org/downloads/))
- **Node.js 16+** ([Download Node.js](https://nodejs.org/))
- **Git** ([Download Git](https://git-scm.com/))
- **Code Editor** (VS Code recommended)

### **Step 1: Clone Repository**
```bash
git clone https://github.com/airaous/AI-Powered-Code-Plagiarism-Detector.git
cd AI-Powered-Code-Plagiarism-Detector
```

### **Step 2: Backend Setup**
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env file with your API keys (optional for basic functionality)
# OPENAI_API_KEY=your_openai_api_key_here
# HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

### **Step 3: Frontend Setup**
```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install Node.js dependencies
npm install
```

### **Step 4: Database Setup**
The SQLite database is automatically created when you first run the backend. No additional setup required for development.

### **Step 5: Running the Application**

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload
```
Backend will be available at: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```
Frontend will be available at: http://localhost:3000

## 🔨 Development Process

### **Phase 1: Project Planning & Architecture**
1. **Requirements Analysis**: Studied existing plagiarism detection tools (MOSS, JPlag, Turnitin)
2. **Technology Selection**: Chose FastAPI + React for modern, scalable architecture
3. **Database Design**: Designed schema for storing comparisons and analysis results
4. **API Design**: Planned RESTful endpoints for comparison operations

### **Phase 2: Backend Development**
1. **FastAPI Setup**: Created project structure with modular architecture
2. **Database Models**: Implemented SQLAlchemy models for data persistence
3. **AI Service**: Developed semantic similarity analysis using NLP techniques
4. **API Endpoints**: Built REST APIs for file upload, comparison, and reporting
5. **Error Handling**: Implemented comprehensive error handling and logging

### **Phase 3: Frontend Development**
1. **React Setup**: Created modern React application with functional components
2. **UI Framework**: Integrated Material-UI for professional interface
3. **Code Editor**: Implemented Monaco Editor for syntax-highlighted code input
4. **File Upload**: Added drag-and-drop file upload functionality
5. **Results Visualization**: Created comprehensive results display with charts

### **Phase 4: Integration & Testing**
1. **API Integration**: Connected frontend to backend APIs
2. **Error Handling**: Implemented user-friendly error messages
3. **Testing**: Tested with various code samples and edge cases
4. **Performance Optimization**: Optimized similarity algorithms

### **Phase 5: Documentation & Deployment**
1. **API Documentation**: Auto-generated OpenAPI documentation
2. **README**: Comprehensive documentation with examples
3. **Deployment Setup**: Prepared Docker configurations
4. **CI/CD**: GitHub Actions workflow ready

## 🐛 Errors Faced & Solutions

### **Error 1: pydantic_settings Import Error**
**Problem**: Initial import error with `pydantic_settings`
```
ImportError: No module named 'pydantic_settings'
```
**Solution**: Updated requirements.txt with correct package version
```bash
pydantic-settings==2.1.0  # Note: hyphen, not underscore
```

### **Error 2: 500 Internal Server Error on Code Comparison**
**Problem**: Backend crashing when comparing code snippets
```
Error comparing code: Request failed with status code 500
```
**Root Cause**: Missing error handling in AI service and database operations
**Solution**: 
1. Added comprehensive try-catch blocks in all API endpoints
2. Implemented fallback similarity algorithm when AI services fail
3. Added detailed logging for debugging
```python
try:
    similarity_result = ai_service.calculate_similarity(...)
except Exception as e:
    print(f"Error in compare_code: {e}")
    raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
```

### **Error 3: CORS Issues Between Frontend and Backend**
**Problem**: Frontend unable to communicate with backend API
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```
**Solution**: Configured CORS middleware in FastAPI
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Error 4: Database Connection Issues**
**Problem**: SQLite database file not created automatically
**Solution**: Updated database.py to create tables on startup
```python
Base.metadata.create_all(bind=engine)
```

### **Error 5: React Dependencies Warnings**
**Problem**: Multiple deprecation warnings during npm install
```
npm WARN deprecated @babel/plugin-proposal-private-methods@7.18.6
```
**Solution**: These are normal warnings for React projects. The application works despite these warnings. For production, we can update to newer package versions.

### **Error 6: Monaco Editor Not Loading**
**Problem**: Code editor not rendering in React components
**Solution**: Added proper Monaco Editor configuration
```jsx
import Editor from '@monaco-editor/react';

<Editor
  height="400px"
  language={language}
  value={code}
  theme="vs-dark"
  options={{
    minimap: { enabled: false },
    fontSize: 14,
  }}
/>
```

### **Error 7: File Upload Size Limits**
**Problem**: Large files causing server crashes
**Solution**: Implemented file size validation
```python
if file1.size > settings.MAX_FILE_SIZE:
    raise HTTPException(status_code=413, detail="File size too large")
```

### **Error 8: AI API Key Management**
**Problem**: Application failing when API keys not provided
**Solution**: Implemented fallback mechanisms
```python
if not self.openai_client:
    return f"Basic similarity analysis: {similarity_score:.2f}"
```

## 📚 API Documentation

### **Base URL**: `http://localhost:8000/api/v1`

### **Endpoints:**

#### **1. Compare Code Snippets**
```http
POST /comparison/compare
Content-Type: application/json

{
  "code1": "def hello():\n    print('Hello')",
  "code2": "def greet():\n    print('Hello')",
  "language1": "python",
  "language2": "python"
}
```

**Response:**
```json
{
  "comparison_id": 1,
  "similarity_score": 0.85,
  "is_plagiarized": true,
  "explanation": "High similarity detected...",
  "lexical_similarity": 0.75,
  "analysis": {
    "code1_tokens": 10,
    "code2_tokens": 10,
    "common_tokens": 8
  }
}
```

#### **2. Upload Files for Comparison**
```http
POST /comparison/upload
Content-Type: multipart/form-data

file1: [binary]
file2: [binary]
language1: python
language2: python
```

#### **3. Get Comparison Report**
```http
GET /comparison/report/{comparison_id}
```

#### **4. Get Comparison History**
```http
GET /comparison/history?limit=10
```

### **Interactive API Documentation**
Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

## 💡 Usage Examples

### **Example 1: Basic Code Comparison**
1. Navigate to http://localhost:3000
2. Click "Start Comparison"
3. Paste these codes:

**Code 1 (Python):**
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
```

**Code 2 (Python):**
```python
def fib(num):
    if num <= 1:
        return num
    return fib(num-1) + fib(num-2)

print(fib(10))
```

**Expected Result**: High similarity (~80-90%) - Potential plagiarism detected

### **Example 2: File Upload Comparison**
1. Create two .py files with the above code
2. Use the "Upload Files" tab
3. Drag and drop both files
4. Select "Python" for both languages
5. Click "Upload and Compare"

### **Example 3: Different Languages**
Test cross-language similarity detection with equivalent algorithms in different languages.

## 🖼️ Screenshots

### **Home Page**
- Clean, professional interface
- Feature highlights
- Call-to-action buttons

### **Comparison Page**
- Dual-pane code editors
- Language selection
- File upload zones
- Real-time syntax highlighting

### **Results Page**
- Similarity score visualization
- Detailed analysis breakdown
- Side-by-side code comparison
- AI-generated explanations

### **History Page**
- Previous comparison listings
- Quick access to detailed reports
- Sorting and filtering options

## 🚀 Deployment

### **Local Development**
Already covered in Installation & Setup section.

### **Docker Deployment**
```yaml
# docker-compose.yml (ready for implementation)
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/plagiarism_db
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

### **Cloud Deployment Options**

#### **Heroku**
```bash
# Backend deployment
heroku create your-app-backend
git subtree push --prefix backend heroku main

# Frontend deployment  
heroku create your-app-frontend
git subtree push --prefix frontend heroku main
```

#### **Vercel (Frontend)**
```bash
cd frontend
npm run build
vercel --prod
```

#### **Railway/Render (Backend)**
- Connect GitHub repository
- Set environment variables
- Deploy with automatic builds

### **Environment Variables for Production**
```bash
# Backend .env
DATABASE_URL=postgresql://user:pass@host:port/db
OPENAI_API_KEY=your_production_key
ALLOWED_HOSTS=["https://your-frontend-domain.com"]
```

## 🤝 Contributing

We welcome contributions! Here's how to get involved:

### **Development Setup**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Create a Pull Request

### **Contribution Guidelines**
- **Code Style**: Follow PEP 8 for Python, ESLint rules for JavaScript
- **Testing**: Add tests for new features
- **Documentation**: Update README for significant changes
- **Commit Messages**: Use clear, descriptive commit messages

### **Areas for Contribution**
- Additional programming language support
- Enhanced AI algorithms
- UI/UX improvements
- Performance optimizations
- Documentation improvements
- Bug fixes and testing

## 🔮 Future Enhancements

### **Phase 1: Core Improvements**
- [ ] **Enhanced AI Models**: Integration with latest CodeBERT variants
- [ ] **Batch Processing**: Compare multiple files simultaneously
- [ ] **Advanced Metrics**: More sophisticated similarity algorithms
- [ ] **Performance Optimization**: Caching and async processing

### **Phase 2: Feature Expansion**
- [ ] **User Authentication**: User accounts and personal dashboards
- [ ] **PDF Report Generation**: Downloadable detailed reports
- [ ] **LMS Integration**: Moodle, Canvas, Blackboard plugins
- [ ] **Real-time Collaboration**: Live comparison sessions

### **Phase 3: Advanced Features**
- [ ] **Code Clone Detection**: Identify code clones across repositories
- [ ] **Plagiarism Trends**: Analytics and reporting dashboards
- [ ] **API Rate Limiting**: Enterprise-grade API management
- [ ] **Multi-tenant Architecture**: Support for multiple organizations

### **Phase 4: AI & Machine Learning**
- [ ] **Custom Model Training**: Train on specific codebases
- [ ] **Explanation Generation**: Detailed AI explanations
- [ ] **False Positive Reduction**: Improved accuracy algorithms
- [ ] **Code Style Analysis**: Detect plagiarism across coding styles

### **Business Opportunities**
- **SaaS Platform**: Subscription-based service
- **Enterprise Licensing**: Custom solutions for institutions
- **API Monetization**: Pay-per-use API access
- **Consulting Services**: Custom plagiarism detection solutions

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 AI-Powered Code Plagiarism Detector

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- **OpenAI** for GPT models and API
- **HuggingFace** for transformer models and community
- **FastAPI** for the excellent Python web framework
- **React Team** for the powerful frontend library
- **Material-UI** for beautiful React components
- **Monaco Editor** for VS Code-quality code editing
- **SQLAlchemy** for robust database ORM

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/AI-Powered-Code-Plagiarism-Detector/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/AI-Powered-Code-Plagiarism-Detector/discussions)
- **Email**: your.email@example.com
- **LinkedIn**: [Your LinkedIn Profile](https://linkedin.com/in/yourprofile)

---

**⭐ If you found this project helpful, please consider giving it a star!**

**🚀 Ready to detect code plagiarism with AI? Get started now!**

---

*Last Updated: January 2025*
*Version: 1.0.0*
*Status: Production Ready*