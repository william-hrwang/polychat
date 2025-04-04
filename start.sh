#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if conda is installed
if ! command_exists conda; then
    echo "❌ Conda is not installed. Please install Conda first."
    exit 1
fi

# Check if the conda environment exists
if ! conda env list | grep -q "polychat"; then
    echo "❌ Conda environment 'polychat' not found. Please create it first."
    exit 1
fi

# Function to start backend services
start_backend() {
    echo "🚀 Starting backend services..."
    
    # Activate conda environment
    eval "$(conda shell.bash hook)"
    conda activate polychat
    
    # Start translation service
    cd backend/translation
    python server.py &
    TRANSLATION_PID=$!
    echo "✅ Translation service started (PID: $TRANSLATION_PID)"
    
    # Start chat service
    cd ../gateway
    python server.py &
    CHAT_PID=$!
    echo "✅ Chat service started (PID: $CHAT_PID)"
    
    # Start auth service
    cd ../auth
    python server.py &
    AUTH_PID=$!
    echo "✅ Auth service started (PID: $AUTH_PID)"
    
    # Start TTS service
    cd ../tts
    python server.py &
    TTS_PID=$!
    echo "✅ TTS service started (PID: $TTS_PID)"
    
    # Return to project root
    cd ../..
    
    # Store PIDs for cleanup
    echo $TRANSLATION_PID > .translation.pid
    echo $CHAT_PID > .chat.pid
    echo $AUTH_PID > .auth.pid
    echo $TTS_PID > .tts.pid
}

# Function to start frontend
start_frontend() {
    echo "🚀 Starting frontend..."
    
    # Check if Node.js is installed
    if ! command_exists node; then
        echo "❌ Node.js is not installed. Please install Node.js first."
        exit 1
    fi
    
    # Check if npm is installed
    if ! command_exists npm; then
        echo "❌ npm is not installed. Please install npm first."
        exit 1
    fi
    
    # Install dependencies if needed
    if [ ! -d "frontend/node_modules" ]; then
        echo "📦 Installing frontend dependencies..."
        cd frontend
        npm install
        cd ..
    fi
    
    # Start frontend
    cd frontend
    node client.js &
    FRONTEND_PID=$!
    echo "✅ Frontend started (PID: $FRONTEND_PID)"
    
    # Return to project root
    cd ..
    
    # Store PID for cleanup
    echo $FRONTEND_PID > .frontend.pid
}

# Function to clean up processes on exit
cleanup() {
    echo "🧹 Cleaning up processes..."
    
    # Kill backend processes
    if [ -f ".translation.pid" ]; then
        kill $(cat .translation.pid) 2>/dev/null || true
        rm .translation.pid
    fi
    
    if [ -f ".chat.pid" ]; then
        kill $(cat .chat.pid) 2>/dev/null || true
        rm .chat.pid
    fi
    
    if [ -f ".auth.pid" ]; then
        kill $(cat .auth.pid) 2>/dev/null || true
        rm .auth.pid
    fi
    
    if [ -f ".tts.pid" ]; then
        kill $(cat .tts.pid) 2>/dev/null || true
        rm .tts.pid
    fi
    
    # Kill frontend process
    if [ -f ".frontend.pid" ]; then
        kill $(cat .frontend.pid) 2>/dev/null || true
        rm .frontend.pid
    fi
    
    # Deactivate conda environment
    eval "$(conda shell.bash hook)"
    conda deactivate
    
    echo "✅ Cleanup complete"
    exit 0
}

# Set up trap to catch Ctrl+C and other termination signals
trap cleanup SIGINT SIGTERM EXIT

# Start all services
start_backend
start_frontend

# Keep the script running
echo "✅ All services started. Press Ctrl+C to stop."
echo "🌐 Frontend is available at http://localhost:8080"
echo "🔌 Backend services are running on ports 50051-50054"

# Wait for user to press Ctrl+C
while true; do
    sleep 1
done 