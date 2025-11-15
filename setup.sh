#!/bin/bash

# AutoLab Drive Setup Script
# This script sets up both backend and frontend

set -e  # Exit on error

echo "🚀 Setting up AutoLab Drive..."
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo "✓ Node.js found: $(node --version)"
echo ""

# Backend setup
echo "🐍 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "  Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "  Installing Python dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "  Creating .env file..."
    cp ../.env.example .env
fi

# Create storage directories
echo "  Creating storage directories..."
mkdir -p storage/datasets storage/frames

# Initialize database
echo "  Initializing database..."
python -m app.db.init_db

echo "✓ Backend setup complete!"
echo ""

# Frontend setup
echo "⚛️  Setting up frontend..."
cd ../frontend

# Install dependencies
echo "  Installing npm dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "  Creating .env file..."
    cp .env.example .env
fi

echo "✓ Frontend setup complete!"
echo ""

# Create sample dataset
echo "📦 Creating sample dataset..."
cd ..
python scripts/create_sample_dataset.py -o sample_dataset.zip -n 100

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo ""
echo "1. Start the backend (in one terminal):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "2. Start the frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open http://localhost:5173 in your browser"
echo ""
echo "4. Upload the sample dataset: sample_dataset.zip"
echo ""
echo "📚 For more information, see QUICKSTART.md"
