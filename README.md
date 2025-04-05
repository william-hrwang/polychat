# PolyChat

PolyChat is a real-time multilingual chat application that enables seamless communication between users speaking different languages. The application features automatic translation, text-to-speech capabilities, and a modern user interface.

## Features

- **Real-time Multilingual Chat**
  - Automatic translation between multiple languages
  - Support for English, French, and Chinese
  - Real-time message delivery
  - Message history preservation
  - Original and translated text display

- **Text-to-Speech (TTS)**
  - Convert messages to speech
  - Play messages in their original language
  - Support for multiple languages
  - Volume control button positioned for easy access
  - Audio processing status indicators

- **User Authentication & Profiles**
  - Secure user registration and login
  - User profiles with avatars
  - Online/offline status tracking
  - Last seen timestamps
  - Profile customization options

- **Chat Features**
  - Public chatroom
  - Message history
  - Real-time message updates
  - Message timestamps
  - User avatars
  - Responsive design for all devices
  - Modern UI with smooth animations

- **RAFT**
  - Leader Election: The system uses the Raft consensus protocol to elect a leader among a cluster of nodes. Only the leader is authorized to process and append new messages, ensuring there’s a single source of truth for the log.
    
  - Replicated Log: When the leader receives a new message, it serializes the message (using JSON) and appends it to a replicated log. This log is stored across all nodes using the Raftos library, which handles the replication process.     The replicated log guarantees that every node in the cluster eventually has an identical copy of the messages, even if some nodes temporarily go offline.
    
  - Fault Tolerance: If the current leader fails or becomes unreachable, the Raft protocol automatically elects a new leader. This ensures that the system remains available and that the message log stays consistent despite node       
    failures.
    
  - Message Propagation: Once a message is appended to the log by the leader, it is streamed to connected clients (via WebSockets) so that every user sees the updated chat history. This replication mechanism ensures that the chat   
    remains synchronized across multiple instances of the application.
 

- **Backup System**
  - Automatic Database Backup: After every critical operation (e.g., registration, login, profile update, avatar upload), the system creates a fresh backup of users.db as users_backup.db. 
  
  - Self-Healing on Startup: On initialization, the service checks if users.db is missing or corrupted. 
    - If it is, the service automatically restores it from the latest users_backup.db. 
    - Resilience Against Data Loss 
    - Ensures high availability of authentication services by maintaining a real-time synced backup.
  - Developer-Friendly Logging 
  - Clear and consistent console logs at each stage (registration, backup, restoration, etc.) to aid in debugging and monitoring. 
  - Ready for Runtime Fallback (Extendable) 
  - The system is structured so runtime backup restoration logic can be added in future, allowing recovery even if the database is lost during operation.

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
  - Translate Service (gRPC): Use Google Translate API to translate message

## Prerequisites

- Python 3.9
- Node.js 14+
- gRPC tools
- FFmpeg (for audio processing)
- Modern web browser with WebSocket support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/polychat.git
cd polychat
git checkout RAFT-2
```

2. Install backend dependencies:
```bash
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
python3 -m grpc_tools.protoc -I gateway --python_out=gateway --grpc_python_out=gateway gateway/chat.proto
python3 -m grpc_tools.protoc -I translation --python_out=translation --grpc_python_out=translation translation/translate.proto
python3 -m grpc_tools.protoc -I tts --python_out=tts --grpc_python_out=tts tts/tts.proto
python3 -m grpc_tools.protoc -I auth --python_out=auth --grpc_python_out=auth auth/auth.proto
```

## Running the Application

1. Start the backend services:
```bash
# Start RAFT node 1 2 3
cd backend/gateway

# Node 1 (Leader)
python3 server.py 1 2 3

# Node 2 (Follower)
python3 server.py 2 1 3

# Node 3 (Follower)
python3 server.py 3 1 2

# Start TTS Service
cd backend/tts
python3 server.py

# Start Auth Service
cd backend/auth
python3 server.py

# Start Translate Service
cd backend/translation
python3 server.py

# Start Chat Service
cd backend/gateway
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
2. Select your preferred language from the dropdown (English, French, or Chinese)
3. Type your message and press Enter or click Send
4. Messages will be automatically translated to the recipient's language
5. Use the 🔊 button (positioned on the right of each message) to play the audio version
6. View other users' online status
7. Messages will show both original and translated text when applicable

## API Endpoints

### Authentication
- `POST /api/register`: Register a new user
- `POST /api/login`: Log in with credentials
- `GET /api/profile`: Get user profile
- `PUT /api/profile`: Update user profile
- `POST /api/logout`: Log out current user

### Chat
- WebSocket connection for real-time messaging
- Message history retrieval
- Audio processing and delivery

## Contributing

The project is contributed by UWO CS9644 Group 6

## Acknowledgments

- gRPC for the microservices architecture
- WebSocket for real-time communication
- Google Cloud Translation API for language translation
- Google Cloud Text-to-Speech API for voice synthesis
- Inter font family for modern typography 