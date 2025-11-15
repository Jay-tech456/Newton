#!/bin/bash

# Frontend Installation Script

set -e

echo "🎨 Installing AutoLab Drive Frontend..."
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 18 or higher from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version is too old: $(node --version)"
    echo "Please upgrade to Node.js 18 or higher"
    exit 1
fi

echo "✓ Node.js $(node --version)"
echo "✓ npm $(npm --version)"
echo ""

# Clean previous installation
if [ -d "node_modules" ]; then
    echo "🧹 Cleaning previous installation..."
    rm -rf node_modules package-lock.json
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

echo ""
echo "✅ Frontend installation complete!"
echo ""
echo "🚀 Start the development server:"
echo "   npm run dev"
echo ""
echo "🌐 The app will be available at:"
echo "   http://localhost:5173"
echo ""
