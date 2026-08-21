#!/bin/bash
echo "🚀 Starting Dar Al-Adeeb Environment Setup..."

# Force SQLite for local/testing development so it doesn't try to connect to Postgres
export DB_ENGINE=django.db.backends.sqlite3
export DB_NAME=db.sqlite3
export DB_USER=
export DB_PASSWORD=
export DB_HOST=
export DB_PORT=
export REDIS_URL=
export CELERY_BROKER_URL=

# Ensure we have a virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Run migrations
echo "🗄️ Preparing Database..."
python manage.py makemigrations
python manage.py migrate

# Collect static files (Very important for PythonAnywhere & Production)
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Setup Complete!"

# If not running on PythonAnywhere, start the dev server
if [[ "$PWD" != *"pythonanywhere"* ]]; then
    echo "🌐 Starting local development server..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "🌍 Running on PythonAnywhere environment."
    echo "💡 Please reload your web app from the PythonAnywhere 'Web' tab."
fi
