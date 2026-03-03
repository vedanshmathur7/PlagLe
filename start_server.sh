#!/bin/bash
# PlagLe API - Quick Start Script

echo "🚀 PlagLe API - Starting Server"
echo "================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo "✅ Please edit .env with your database credentials"
    echo "   Then run this script again."
    exit 1
fi

# Check if dependencies are installed
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt

# Ensure directories exist
echo "📁 Creating necessary directories..."
mkdir -p uploads reports logs

# Check database connection (optional)
echo "🔍 Checking database connection..."
python -c "
import mysql.connector
from app.core.config import get_settings

settings = get_settings()
try:
    conn = mysql.connector.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )
    conn.close()
    print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    print('   Please check your .env configuration')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo ""
    echo "Please fix the database connection and try again."
    exit 1
fi

echo ""
echo "✅ All checks passed!"
echo ""
echo "🎉 Starting FastAPI server..."
echo "================================"
echo ""
echo "📍 Server will be available at:"
echo "   - API: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo "   - Redoc: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
