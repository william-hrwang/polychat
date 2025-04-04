#!/bin/bash

echo "🛑 Stopping all services..."

# Function to kill a process by PID file
kill_process() {
    local pid_file=$1
    local service_name=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null; then
            echo "🛑 Stopping $service_name service (PID: $pid)..."
            kill $pid
            rm "$pid_file"
            echo "✅ $service_name service stopped"
        else
            echo "⚠️ $service_name service already stopped"
            rm "$pid_file"
        fi
    else
        echo "⚠️ No PID file found for $service_name service"
    fi
}

# Kill backend services
kill_process ".translation.pid" "Translation"
kill_process ".chat.pid" "Chat"
kill_process ".auth.pid" "Auth"
kill_process ".tts.pid" "TTS"

# Kill frontend service
kill_process ".frontend.pid" "Frontend"

# Deactivate conda environment
eval "$(conda shell.bash hook)"
conda deactivate

echo "✅ All services stopped" 