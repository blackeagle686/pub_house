#!/bin/bash
echo "🚀 Starting Dar Al-Adeeb Deployment Environment (Docker)..."

# If docker-compose is installed, build and run detached
echo "Building Docker images and starting services (Postgres, Redis, Celery, Django)..."
docker-compose up --build -d

echo "✅ Services are up and running!"
echo "----------------------------------------"
echo "🌐 Web App: http://localhost:8000"
echo "📜 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"
echo "----------------------------------------"
