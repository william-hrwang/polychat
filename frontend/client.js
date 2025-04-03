const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const WebSocket = require('ws');
const http = require('http');
const fs = require('fs');
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');

// Load proto files
const chatPackageDef = protoLoader.loadSync(path.join(__dirname, 'grpc/chat.proto'));
const chatProto = grpc.loadPackageDefinition(chatPackageDef).chat;

const ttsPackageDef = protoLoader.loadSync(path.join(__dirname, 'grpc/tts.proto'));
const ttsProto = grpc.loadPackageDefinition(ttsPackageDef).tts;

const authPackageDef = protoLoader.loadSync(path.join(__dirname, 'grpc/auth.proto'));
const authProto = grpc.loadPackageDefinition(authPackageDef).auth;

// gRPC clients
const chatClient = new chatProto.ChatService(
  'localhost:50052', grpc.credentials.createInsecure()
);

const ttsClient = new ttsProto.TTSService(
  'localhost:50054', grpc.credentials.createInsecure()
);

const authClient = new authProto.AuthService(
  'localhost:50053', grpc.credentials.createInsecure()
);

// Connected WebSocket clients
const clients = new Map(); // username -> WebSocket

// Express app for API endpoints
const app = express();
app.use(bodyParser.json());

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Deckard Add, Status Check
// Store user status information
let userPresenceData = [];
const PRESENCE_UPDATE_INTERVAL = 10000; // 10 seconds

// Authentication middleware
const authenticateToken = (req, res, next) => {
  const token = req.headers['authorization'].split(' ')[1];
  if (!token) {
    return res.status(401).json({ success: false, message: 'No token provided' });
  }

  authClient.VerifyToken({ token }, (err, response) => {
    if (err || !response.success) {
      return res.status(401).json({ success: false, message: 'Invalid token' });
    }
    req.user = response.username;
    next();
  });
};

// API Routes
app.post('/api/register', (req, res) => {
  authClient.Register(req.body, (err, response) => {
    if (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
    res.json(response);
  });
});

app.post('/api/login', (req, res) => {
  authClient.Login(req.body, (err, response) => {
    if (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
    res.json(response);
  });
});

app.get('/api/profile', authenticateToken, (req, res) => {
  authClient.GetProfile({ username: req.user, token: req.headers['authorization'].split(' ')[1] }, (err, response) => {
    if (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
    res.json(response);
  });
});

app.put('/api/profile', authenticateToken, (req, res) => {
  authClient.UpdateProfile({
    username: req.user,
    token: req.headers['authorization'].split(' ')[1],
    ...req.body
  }, (err, response) => {
    if (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
    res.json(response);
  });
});

app.post('/api/logout', authenticateToken, (req, res) => {
  authClient.Logout({ 
    username: req.user, 
    token: req.headers['authorization'].split(' ')[1] 
  }, (err, response) => {
    if (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
    res.json(response);
  });
});

// Deckard Add, Status Check
// Add new API route to get all users
app.get('/api/users', authenticateToken, (req, res) => {
  authClient.GetAllUsers({ token: req.headers['authorization'].split(' ')[1] }, (err, response) => {
    if (err) {
      return res.status(500).json({ success: false, message: err.message });
    }
    res.json(response);
  });
});

// Create HTTP server
const server = http.createServer(app);

// WebSocket server
const wss = new WebSocket.Server({ server });

// Store chat history
let chatHistory = [];

// Deckard Add, Status Check
// Function to update and broadcast user presence
function updateAndBroadcastPresence() {
  // Use server admin token or generate a special token for this purpose
  // For prototype, we'll use the first connected client's token
  if (clients.size === 0) {
    console.log('No clients connected, skipping presence update');
    return;
  }
  
  const someClient = Array.from(clients.values())[0];
  if (!someClient || !someClient.token) {
    console.error('No valid client token available for presence update');
    return;
  }
  
  const someToken = someClient.token;
  
  authClient.GetAllUsers({ token: someToken }, (err, response) => {
    if (err) {
      console.error('Failed to fetch user presence:', err);
      return;
    }
    
    //Deckard Add, Status Check
    if (!response || !response.success) {
      console.error('Failed to fetch user presence:', response ? response.message : 'No response');
      return;
    }
    
    // Ensure users is always an array, even if empty
    userPresenceData = Array.isArray(response.users) ? response.users : [];
    
    // Broadcast presence update to all clients
    const presencePayload = JSON.stringify({ 
      type: 'presence', 
      users: userPresenceData 
    });
    
    let sentCount = 0;
    clients.forEach((client) => {
      if (client.ws && client.ws.readyState === WebSocket.OPEN) {
        client.ws.send(presencePayload);
        sentCount++;
      }
    });
    
    console.log(`Broadcasted presence data for ${userPresenceData.length} users to ${sentCount} clients`);
  });
}

// Start presence update interval
const presenceInterval = setInterval(updateAndBroadcastPresence, PRESENCE_UPDATE_INTERVAL);

wss.on('connection', (ws, req) => {
  const token = new URL(req.url, 'http://localhost').searchParams.get('token');
  
  if (!token) {
    console.log('No token provided in WebSocket connection');
    ws.close(1008, 'Authentication required');
    return;
  }

  console.log('New WebSocket connection attempt with token');
  
  authClient.VerifyToken({ token }, (err, response) => {
    if (err || !response.success) {
      console.error('Token verification failed:', err || response);
      ws.close(1008, 'Invalid token');
      return;
    }

    const username = response.username;
    console.log(`🧠 New client connected: ${username}`);
    
    // Store client connection
    clients.set(username, { ws, token }); // Store token with WebSocket //Deckard Add, Status Check

    // Send chat history to new client
    if (chatHistory.length > 0) {
      console.log(`Sending ${chatHistory.length} messages of history to ${username}`);
      ws.send(JSON.stringify({ type: 'history', messages: chatHistory }));
    }

    // Deckard Add, Status Check
    // Send initial presence data to new client
    if (userPresenceData.length > 0) {
      ws.send(JSON.stringify({ 
        type: 'presence', 
        users: userPresenceData 
      }));
    }

    // Update online status
    authClient.UpdateProfile({
      username,
      token,
      is_online: true,
      last_seen: new Date().toISOString()
    }, (err, response) => {
      if (err) {
        console.error('Failed to update online status:', err);
      }
    });

    ws.on('message', (data) => {
      try {
        const message = JSON.parse(data);
        console.log(`Received message from ${username}:`, message);
        
        chatClient.SendMessage({
          username: message.username,
          message: message.message,
          language: message.language
        }, (err, res) => {
          if (err) console.error('Error sending message to chat service:', err);
        });
      } catch (err) {
        console.error('Error processing WebSocket message:', err);
      }
    });

    ws.on('close', () => {
      console.log(`👋 Client disconnected: ${username}`);
      clients.delete(username);
      
      // Update offline status
      authClient.UpdateProfile({
        username,
        token,
        is_online: false,
        last_seen: new Date().toISOString()
      }, (err, response) => {
        if (err) {
          console.error('Failed to update offline status:', err);
        }
      });
    });
  });
});

// gRPC stream: receive messages and broadcast
const stream = chatClient.StreamMessages({ username: 'server' });

stream.on('data', (msg) => {
  console.log("📥 Received from gRPC stream:", msg);
  
  // Add message to chat history
  chatHistory.push(msg);
  
  // Keep only last 100 messages
  if (chatHistory.length > 100) {
    chatHistory = chatHistory.slice(-100);
  }
  
  // Broadcast text message to all connected clients
  const textPayload = JSON.stringify({ type: 'message', ...msg });
  clients.forEach((client) => {
    if (client.ws.readyState === WebSocket.OPEN) {//Deckard Add, Status Check
      client.ws.send(textPayload);//Deckard Add, Status Check
    }
  });
  
  // Call TTS
  ttsClient.TextToSpeech({ text: msg.message }, (err, response) => {
    if (err) {
      console.error("TTS error:", err);
      return;
    }
    
    console.log("📦 TTS raw response:", response);
    
    if (!response || !response.audioData) {
      console.warn("⚠️ No audio data received from TTS service.");
      return;
    }
    
    const audioData = response.audioData.toString('base64');
    const audioPayload = JSON.stringify({ type: 'audio', audio: audioData });
    clients.forEach((client) => {
      if (client.ws.readyState === WebSocket.OPEN) {//Deckard Add, Status Check
        client.ws.send(audioPayload);//Deckard Add, Status Check
      }
    });
  });
});

// Deckard Add, Status Check
// Cleanup on server shutdown
server.on('close', () => {
  clearInterval(presenceInterval);
  clients.clear();
});

// Start server
const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}`);
});


// grpcClient.SendMessage({
//     username: 'test_user',
//     message: 'Hello World!',
//     language: 'en'
//   }, (err, res) => {
//     if (err) console.error("SendMessage error:", err);
//     else console.log("✅ Message sent!");
//   });



  