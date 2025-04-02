# PolyChat

PolyChat is a real-time multilingual chat application that enables seamless communication between users speaking different languages. The application features automatic translation, text-to-speech capabilities, and a modern user interface.

## Features

- 🌐 **Real-time Multilingual Chat**
  - Automatic translation between multiple languages
  - Support for English, French, and Chinese
  - Real-time message delivery

- 🔊 **Text-to-Speech (TTS)**
  - Convert messages to speech
  - Play messages in their original language
  - Support for multiple languages

- 👤 **User Authentication & Profiles**
  - Secure user registration and login
  - User profiles with avatars
  - Online/offline status tracking
  - Last seen timestamps

- 💬 **Chat Features**
  - Public chatroom
  - Message history
  - Real-time message updates
  - Message timestamps
  - User avatars

## Architecture

The application is built using a microservices architecture:

- **Frontend**: Node.js with WebSocket for real-time communication
- **Backend Services**:
  - Chat Service (gRPC): Handles message routing and translation
  - TTS Service (gRPC): Converts text to speech
  - Auth Service (gRPC): Manages user authentication and profiles

## Prerequisites

- Python 3.7+
- Node.js 14+
- gRPC tools
- FFmpeg (for audio processing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/polychat.git
cd polychat
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Generate gRPC code:
```bash
cd backend
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tts.proto
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. auth.proto
```

## Running the Application

1. Start the backend services:
```bash
# Start Chat Service
cd backend/chat
python3 server.py

# Start TTS Service
cd backend/tts
python3 server.py

# Start Auth Service
cd backend/auth
python3 server.py
```

2. Start the frontend server:
```bash
cd frontend
node client.js
```

3. Open your browser and navigate to:
```
http://localhost:8080
```

## Usage

1. Register a new account or log in with existing credentials
2. Select your preferred language from the dropdown
3. Type your message and press Enter or click Send
4. Messages will be automatically translated and can be played using the 🔊 button
5. View other users' online status and last seen times
6. Update your profile information and avatar

## API Endpoints

### Authentication
- `POST /api/register`: Register a new user
- `POST /api/login`: Log in with credentials
- `GET /api/profile`: Get user profile
- `PUT /api/profile`: Update user profile
- `POST /api/logout`: Log out current user

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- gRPC for the microservices architecture
- WebSocket for real-time communication
- Google Cloud Translation API for language translation
- Google Cloud Text-to-Speech API for voice synthesis 