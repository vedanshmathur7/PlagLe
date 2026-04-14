# 🎓 PlagLe - Production-Ready Plagiarism Detection API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**A comprehensive, production-ready backend API for detecting plagiarism in student submissions**

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-endpoints) • [Deployment](#-deployment)

</div>

---

## 📋 Overview

PlagLe is a sophisticated plagiarism detection system designed for academic institutions. It provides:
- **Automated plagiarism detection** using TF-IDF cosine similarity
- **PDF report generation** with detailed analysis
- **RESTful API** ready for frontend integration
- **Production-ready architecture** with logging, error handling, and database pooling

### Architecture

```
┌─────────────┐    HTTP     ┌──────────────┐    Business    ┌─────────────────┐
│   Frontend  │ ──────────> │  FastAPI     │ ──────────────> │   Services      │
│   (React)   │             │  Routes      │                 │   Layer         │
└─────────────┘             └──────────────┘                 └─────────────────┘
                                    │                                 │
                                    v                                 v
                            ┌──────────────┐                  ┌─────────────────┐
                            │   Pydantic   │                  │  Core Logic     │
                            │   Schemas    │                  │  (TF-IDF)       │
                            └──────────────┘                  └─────────────────┘
                                    │                                 │
                                    v                                 v
                            ┌──────────────────────────────────────────┐
                            │         MySQL Database                   │
                            │  (Connection Pool + Transaction Mgmt)    │
                            └──────────────────────────────────────────┘
```

---

## ✨ Features

### Core Functionality
- ✅ **Multi-format Support**: TXT, PDF, DOCX file processing
- ✅ **TF-IDF Similarity**: Industry-standard text comparison
- ✅ **Automated Reports**: Professional PDF report generation
- ✅ **Risk Classification**: Low/Medium/High risk categorization
- ✅ **Batch Processing**: Compare against all submissions

### Production Features
- 🚀 **FastAPI Framework**: High-performance async API
- 🔒 **CORS Enabled**: Ready for frontend integration
- 📊 **Request Logging**: Comprehensive request/response tracking
- ⚡ **Connection Pooling**: Optimized database performance
- 🛡️ **Error Handling**: Graceful error management
- 📁 **File Validation**: Size and type checking
- 🐳 **Docker Support**: Containerized deployment ready
- ☁️ **Cloud Ready**: AWS EC2 deployment instructions included

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- MySQL 8.0 or higher
- Git

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd PlagLe

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
python -m nltk.downloader stopwords

# 4. Setup environment
cp .env.example .env
# Edit .env with your database credentials

# 5. Initialize database
mysql -u root -p < schema.sql

# 6. Run the server
uvicorn app.main:app --reload
```

**🎉 Server is now running at:** http://localhost:8000

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

---

## 📁 Project Structure

```
PlagLe/
├── app/                          # FastAPI application
│   ├── main.py                   # Application entry point
│   ├── core/                     # Core functionality
│   │   ├── config.py            # Configuration management
│   │   ├── database.py          # Database connections
│   │   └── logging_config.py   # Logging setup
│   ├── api/                      # API layer
│   │   └── routes.py            # Endpoint definitions
│   ├── services/                 # Business logic
│   │   ├── file_service.py      # File handling
│   │   ├── plagiarism_service.py # Plagiarism detection
│   │   └── report_service.py    # Report generation
│   ├── models/                   # Data models
│   │   └── schemas.py           # Pydantic schemas
│   └── utils/                    # Utilities
│       └── helpers.py
├── similarity_engine.py          # Core ML logic (TF-IDF)
├── report_generator.py           # PDF generation logic
├── schema.sql                    # Database schema
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose setup
├── .env.example                  # Environment template
└── API_DOCUMENTATION.md          # Comprehensive API docs
```

---

## 🔌 API Endpoints

### Primary Endpoint (Recommended)

#### `POST /api/v1/check-plagiarism`
Complete workflow in one call: Upload → Check → Report

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/check-plagiarism" \
  -F "file=@document.txt" \
  -F "assignment_id=1" \
  -F "student_id=2" \
  -F "generated_by=1"
```

**Response:**
```json
{
  "success": true,
  "message": "Plagiarism check completed successfully",
  "document": {
    "document_id": 123,
    "file_name": "document.txt",
    "uploaded_at": "2026-03-03T10:00:00"
  },
  "plagiarism_check": {
    "similarities_found": 2,
    "threshold": 0.15,
    "results": [...]
  },
  "reports": [
    {
      "report_id": 1,
      "report_url": "/api/v1/reports/download/Report_1.pdf"
    }
  ]
}
```

### Additional Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/upload` | Upload file only |
| POST | `/api/v1/plagiarism-check/{doc_id}` | Check existing document |
| POST | `/api/v1/generate-report/{sim_id}` | Generate report |
| GET | `/api/v1/reports/download/{filename}` | Download PDF report |

📚 **Full API Documentation**: See [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start all services (MySQL + API)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

This will:
- Start MySQL database with schema initialization
- Start FastAPI application
- Create necessary volumes for data persistence

---

## ☁️ AWS EC2 Deployment

### Quick Deploy Script

```bash
# On your EC2 instance (Ubuntu)
sudo apt update && sudo apt install -y docker.io docker-compose git
git clone <your-repo>
cd PlagLe
cp .env.example .env
# Edit .env with production values
docker-compose up -d
```

### Complete Deployment Guide

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md#️-aws-ec2-deployment) for:
- EC2 instance setup
- Security group configuration
- Domain and SSL setup
- Nginx reverse proxy
- Production optimization

---

## 🧪 Testing

### Using cURL

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Upload and check plagiarism
curl -X POST http://localhost:8000/api/v1/check-plagiarism \
  -F "file=@test.txt" \
  -F "assignment_id=1" \
  -F "student_id=2" \
  -F "generated_by=1"
```

### Using Python

```python
import requests

with open('document.txt', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/check-plagiarism',
        files={'file': f},
        data={
            'assignment_id': 1,
            'student_id': 2,
            'generated_by': 1
        }
    )
    print(response.json())
```

### React Integration Example

```jsx
const formData = new FormData();
formData.append('file', file);
formData.append('assignment_id', assignmentId);
formData.append('student_id', studentId);
formData.append('generated_by', instructorId);

const response = await fetch('http://localhost:8000/api/v1/check-plagiarism', {
  method: 'POST',
  body: formData,
});

const result = await response.json();
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```env
# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=plagle_db

# Application
DEBUG=False
PORT=8000
SIMILARITY_THRESHOLD=0.15

# CORS (add your frontend URLs)
# Configured in app/core/config.py
```

---

## 📊 Database Schema

The system uses 8 main tables:

- **User**: Students, instructors, admins
- **Course**: Course information
- **Assignment**: Assignment details
- **Submission**: Student submissions
- **Document**: Uploaded files
- **Algorithm**: Comparison algorithms
- **Similarity**: Comparison results
- **Report**: Generated reports

See [schema.sql](schema.sql) for complete structure.

---

## 🛠️ Development

### Running in Development Mode

```bash
# With auto-reload
uvicorn app.main:app --reload --log-level debug

# Or
python -m app.main
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions
- Keep functions focused and modular

### Adding New Features

1. **Create service** in `app/services/`
2. **Define schema** in `app/models/schemas.py`
3. **Add route** in `app/api/routes.py`
4. **Update tests** (if applicable)

---

## 📝 Core Logic

### Plagiarism Detection Algorithm

Uses **TF-IDF (Term Frequency-Inverse Document Frequency)** with **Cosine Similarity**:

1. **Text Extraction**: Extract text from PDF/DOCX/TXT
2. **Preprocessing**: Lowercase, remove punctuation, remove stopwords
3. **Vectorization**: Convert to TF-IDF vectors
4. **Comparison**: Calculate cosine similarity (0.0 - 1.0)
5. **Classification**:
   - < 20%: Low Risk (Green)
   - 20-50%: Medium Risk (Orange)
   - > 50%: High Risk (Red)

Located in: [`similarity_engine.py`](similarity_engine.py)

---

## 🔍 Monitoring & Logs

### Log Files

```bash
# Application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f api
```

### Log Format

```
2026-03-03 10:00:00 - app.main - INFO - Starting PlagLe API v1.0.0
2026-03-03 10:00:01 - app.api.routes - INFO - → POST /api/v1/check-plagiarism
2026-03-03 10:00:05 - app.services.plagiarism_service - INFO - Similarity: 0.7500
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error:**
```bash
# Check MySQL is running
sudo systemctl status mysql
# Check credentials in .env
```

**Port Already in Use:**
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

**Import Errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md#-troubleshooting) for more.

---

## 📖 Documentation

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference, deployment guides, examples
- **[Interactive API Docs](http://localhost:8000/docs)** - Swagger UI (when server is running)
- **[Alternative API Docs](http://localhost:8000/redoc)** - ReDoc UI (when server is running)
- **[PlagLe_User_Guide.md](PlagLe_User_Guide.md)** - Original user guide for instructors

---

## 🎯 Roadmap

- [ ] Add user authentication (JWT)
- [ ] Implement rate limiting
- [ ] Add more similarity algorithms
- [ ] Support for code plagiarism detection
- [ ] WebSocket for real-time progress
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] Bulk file upload
- [ ] API versioning

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Authors

**PlagLe Project**  
DBMS SEM4 Project - 2026

---

## 🙏 Acknowledgments

- FastAPI for the excellent framework
- scikit-learn for TF-IDF implementation
- ReportLab for PDF generation
- MySQL for robust database

---

<div align="center">

**Built with ❤️ for academic integrity**

[⬆ Back to Top](#-plagle---production-ready-plagiarism-detection-api)

</div>
