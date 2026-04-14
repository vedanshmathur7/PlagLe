# PlagLe FastAPI Backend - Comprehensive Documentation

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- Virtual environment tool

### Installation

1. **Clone and navigate to project:**
```bash
cd /home/vedansh/All/SEM4/DBMS/PlagLe
```

2. **Create and activate virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
python -m nltk.downloader stopwords
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Setup database:**
```bash
mysql -u root -p < schema.sql
```

6. **Run the server:**
```bash
# Method 1: Using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Method 2: Using Python
python -m app.main

# Method 3: Using the main module
cd app && python main.py
```

7. **Access the API:**
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

---

## 📁 Project Structure

```
PlagLe/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── core/
│   │   ├── config.py             # Configuration management
│   │   ├── database.py           # Database connection pooling
│   │   └── logging_config.py    # Logging setup
│   ├── api/
│   │   └── routes.py             # API endpoints
│   ├── services/
│   │   ├── file_service.py       # File upload handling
│   │   ├── plagiarism_service.py # Plagiarism detection wrapper
│   │   └── report_service.py     # Report generation wrapper
│   ├── models/
│   │   └── schemas.py            # Pydantic models
│   └── utils/
│       └── helpers.py            # Utility functions
├── similarity_engine.py          # Core plagiarism detection logic
├── report_generator.py           # Core PDF report generation
├── schema.sql                    # Database schema
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── Dockerfile                    # Docker configuration
├── docker-compose.yml            # Docker Compose setup
├── uploads/                      # Uploaded files storage
├── reports/                      # Generated reports
└── logs/                         # Application logs
```

---

## 🔌 API Endpoints

### **Primary Endpoint (All-in-One)**

#### `POST /api/v1/check-plagiarism`
Complete flow: Upload → Check → Generate Reports

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/check-plagiarism" \
  -F "file=@document.txt" \
  -F "assignment_id=1" \
  -F "student_id=2" \
  -F "generated_by=1" \
  -F "algorithm_id=1"
```

**Response:**
```json
{
  "success": true,
  "message": "Plagiarism check completed successfully",
  "document": {
    "document_id": 123,
    "file_name": "document.txt",
    "file_path": "/uploads/...",
    "file_hash": "abc123...",
    "uploaded_at": "2026-03-03T10:00:00"
  },
  "plagiarism_check": {
    "document_id": 123,
    "total_comparisons": 5,
    "similarities_found": 2,
    "threshold": 0.15,
    "results": [
      {
        "similarity_id": 1,
        "score": 0.75,
        "score_percentage": 75.0,
        "risk_level": "High Risk",
        "doc1_name": "document.txt",
        "doc2_name": "other.txt",
        "student1_name": "Alice A",
        "student2_name": "Bob B"
      }
    ]
  },
  "reports": [
    {
      "report_id": 1,
      "similarity_id": 1,
      "report_url": "/api/v1/reports/download/Report_SIM1_20260303_100000.pdf",
      "report_pdf_path": "/reports/...",
      "summary_notes": "High risk of plagiarism detected"
    }
  ]
}
```

### **Individual Endpoints**

#### `POST /api/v1/upload`
Upload file only (without checking)

#### `POST /api/v1/plagiarism-check/{document_id}`
Check plagiarism for existing document

#### `POST /api/v1/generate-report/{similarity_id}`
Generate report for existing similarity

#### `GET /api/v1/reports/download/{filename}`
Download PDF report

#### `GET /api/v1/health`
Health check endpoint

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start all services (MySQL + API)
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t plagle-api .

# Run container
docker run -d \
  -p 8000:8000 \
  -e DB_HOST=your-mysql-host \
  -e DB_PASSWORD=your-password \
  --name plagle-api \
  plagle-api
```

---

## ☁️ AWS EC2 Deployment

### 1. **Launch EC2 Instance**
- AMI: Ubuntu 22.04
- Instance Type: t3.medium (minimum)
- Security Group: Allow ports 22 (SSH), 8000 (API), 3306 (MySQL)

### 2. **Connect and Setup**

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo apt install docker-compose -y

# Clone your repository
git clone https://github.com/your-repo/PlagLe.git
cd PlagLe
```

### 3. **Configure Environment**

```bash
# Create .env file
cp .env.example .env
nano .env

# Update:
# - DB_PASSWORD
# - CORS_ORIGINS (add your frontend URL)
# - DEBUG=False
```

### 4. **Deploy with Docker Compose**

```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 5. **Setup Domain & SSL (Optional)**

```bash
# Install Nginx
sudo apt install nginx -y

# Configure reverse proxy
sudo nano /etc/nginx/sites-available/plagle

# Add:
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable and restart
sudo ln -s /etc/nginx/sites-available/plagle /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Install SSL with Certbot
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_USER` | Database user | `root` |
| `DB_PASSWORD` | Database password | `` |
| `DB_NAME` | Database name | `plagle_db` |
| `PORT` | API server port | `8000` |
| `DEBUG` | Debug mode | `False` |
| `SIMILARITY_THRESHOLD` | Plagiarism threshold | `0.15` |
| `MAX_FILE_SIZE` | Max upload size (bytes) | `10485760` |

---

## 🧪 Testing

### Using cURL

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Upload and check
curl -X POST http://localhost:8000/api/v1/check-plagiarism \
  -F "file=@test.txt" \
  -F "assignment_id=1" \
  -F "student_id=2" \
  -F "generated_by=1"
```

### Using Python

```python
import requests

# Upload and check plagiarism
with open('document.txt', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/check-plagiarism',
        files={'file': f},
        data={
            'assignment_id': 1,
            'student_id': 2,
            'generated_by': 1,
            'algorithm_id': 1
        }
    )
    print(response.json())
```

### Using JavaScript (React)

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('assignment_id', 1);
formData.append('student_id', 2);
formData.append('generated_by', 1);

const response = await fetch('http://localhost:8000/api/v1/check-plagiarism', {
  method: 'POST',
  body: formData,
});

const result = await response.json();
console.log(result);
```

---

## 📊 Monitoring & Logs

### View Logs

```bash
# Application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f api

# Uvicorn access logs
# Automatically displayed in console
```

### Log Format

```
2026-03-03 10:00:00 - app.main - INFO - Starting PlagLe API v1.0.0
2026-03-03 10:00:01 - app.api.routes - INFO - → POST /api/v1/check-plagiarism
2026-03-03 10:00:05 - app.services.plagiarism_service - INFO - Similarity: 0.7500
2026-03-03 10:00:06 - app.api.routes - INFO - ← POST /api/v1/check-plagiarism [200] 5.234s
```

---

## 🛠️ Troubleshooting

### Database Connection Issues

```bash
# Check MySQL is running
sudo systemctl status mysql

# Test connection
mysql -u root -p -e "SELECT 1"

# Check database exists
mysql -u root -p -e "SHOW DATABASES"
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### File Permission Issues

```bash
# Fix permissions
chmod -R 755 uploads reports logs
chown -R $USER:$USER uploads reports logs
```

---

## 🎯 Frontend Integration Guide

### React Example

```jsx
import React, { useState } from 'react';

function PlagiarismChecker() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('assignment_id', 1);
    formData.append('student_id', 2);
    formData.append('generated_by', 1);

    try {
      const response = await fetch('http://localhost:8000/api/v1/check-plagiarism', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button type="submit" disabled={loading}>
          {loading ? 'Checking...' : 'Check Plagiarism'}
        </button>
      </form>

      {result && (
        <div>
          <h3>Results</h3>
          <p>Similarities Found: {result.plagiarism_check.similarities_found}</p>
          {result.reports.map(report => (
            <a key={report.report_id} href={`http://localhost:8000${report.report_url}`} download>
              Download Report
            </a>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## 📝 License & Credits

Built for DBMS SEM4 Project
Plagiarism Detection System using TF-IDF Cosine Similarity

---

## 🆘 Support

For issues or questions:
1. Check logs: `logs/app.log`
2. Test health endpoint: `/api/v1/health`
3. Review API docs: `/docs`
4. Check database connectivity

---

**Happy Coding! 🚀**
