#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Setting up Las Vegas AI development environment..."

# Check Python installation
if ! command_exists python3; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check Node.js installation
if ! command_exists node; then
    echo "Error: Node.js is required but not installed."
    exit 1
fi

# Check PostgreSQL installation
if ! command_exists psql; then
    echo "Error: PostgreSQL is required but not installed."
    exit 1
fi

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
FLASK_APP=backend/app.py
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/vegas_ai
VITE_API_URL=http://localhost:5000
EOL
fi

echo "Setup complete! To start the development servers:"
echo "1. Start the backend: source venv/bin/activate && cd backend && flask run"
echo "2. Start the frontend: cd frontend && npm run dev" 