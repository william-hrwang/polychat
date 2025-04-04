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

# Check if the conda environment already exists
if conda env list | grep -q "polychat"; then
    echo "⚠️ Conda environment 'polychat' already exists."
    read -p "Do you want to recreate it? (y/n): " recreate
    if [ "$recreate" = "y" ]; then
        echo "🗑️ Removing existing 'polychat' environment..."
        conda env remove -n polychat
    else
        echo "✅ Using existing 'polychat' environment."
        exit 0
    fi
fi

# Create conda environment
echo "🔧 Creating conda environment 'polychat'..."
conda create -n polychat python=3.9 -y

# Activate the environment
eval "$(conda shell.bash hook)"
conda activate polychat

# Install required Python packages
echo "📦 Installing Python dependencies..."
pip install grpcio grpcio-tools googletrans==3.1.0a0 gtts PyJWT

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

echo "✅ Setup complete! You can now run the project using './start.sh'" 