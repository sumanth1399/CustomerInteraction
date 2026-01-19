#!/bin/bash

set -e

echo "🚀 Starting Customer Interaction Platform locally..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found in current directory"
    exit 1
fi

echo "📦 Building Docker images (this may take a few minutes)..."
docker-compose build

echo ""
echo "🎬 Starting services..."
docker-compose up

echo ""
echo "✅ Services are running!"
echo ""
echo "🌐 Access the Chat UI at: http://localhost:8001"
echo "🏥 Health Check: http://localhost:8001/health"
echo ""
echo "Press Ctrl+C to stop all services"