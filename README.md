# PolyChat

PolyChat is a real-time multilingual chat application that enables seamless communication between users speaking different languages. The application features automatic translation, text-to-speech capabilities, and a modern user interface.

## Features

- 🌐 **Real-time Multilingual Chat**
  - Automatic translation between multiple languages
  - Support for English, French, and Chinese
  - Real-time message delivery
  - Message history preservation
  - Original and translated text display

- 🔊 **Text-to-Speech (TTS)**
  - Convert messages to speech
  - Play messages in their original language
  - Support for multiple languages
  - Volume control button positioned for easy access
  - Audio processing status indicators

- 👤 **User Authentication & Profiles**
  - Secure user registration and login
  - User profiles with avatars
  - Online/offline status tracking
  - Last seen timestamps
  - Profile customization options

- 💬 **Chat Features**
  - Public chatroom
  - Message history
  - Real-time message updates
  - Message timestamps
  - User avatars
  - Responsive design for all devices
  - Modern UI with smooth animations

   **Backup System
   - when primary database failed, it will swtich to backup system
   - when the primary database are not found, it will copy direct from the backup stored before
   - backup system has syc up with the primary everytime a new record stored

## Architecture

The application is built using a microservices architecture:

- **Frontend**: 
  - Node.js with WebSocket for real-time communication
  - Modern UI with responsive design
  - Client-side message processing and audio handling

- **Backend Services**:
  - Chat Service (gRPC): Handles message routing and translation
  - TTS Service (gRPC): Converts text to speech
  - Auth Service (gRPC): Manages user authentication and profiles

## Prerequisites

- [Conda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution)
- [Node.js](https://nodejs.org/) (v14 or higher)
- [npm](https://www.npmjs.com/) (comes with Node.js)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/polychat.git
   cd polychat
   ```

2. Run the setup script to create the conda environment and install dependencies:
   ```bash
   ./setup.sh
   ```

   This script will:
   - Create a conda environment named 'polychat'
   - Install required Python packages
   - Install Node.js dependencies

## Running the Application

1. Start all services:
   ```bash
   ./start.sh
   ```

   This will start:
   - Translation service (port 50051)
   - Chat service (port 50052)
   - Auth service (port 50053)
   - TTS service (port 50054)
   - Frontend server (port 8080)

2. Access the application:
   - Open your browser and navigate to http://localhost:8080

3. Stop all services:
   ```bash
   ./stop.sh
   ```

## Configuration

The application uses configuration files to manage ports and service connections:

- `config/backend_config.json`: Configuration for backend services
- `config/frontend_config.json`: Configuration for frontend server and service connections

You can modify these files to change ports or host settings.

## Troubleshooting

- If you encounter any issues with the conda environment, try recreating it:
  ```bash
  ./setup.sh
  ```
  When prompted, choose 'y' to recreate the environment.

- If services fail to start, check the logs for error messages.

- If you need to manually stop a service, use the stop script:
  ```bash
  ./stop.sh
  ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- gRPC for the microservices architecture
- WebSocket for real-time communication
- Google Cloud Translation API for language translation
- Google Cloud Text-to-Speech API for voice synthesis
- Inter font family for modern typography 