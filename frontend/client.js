const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const WebSocket = require('ws');
const http = require('http');
const fs = require('fs');
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const multer = require('multer');
<<<<<<< HEAD


// Configure multer to store files in memory and log details
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB limit
=======
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 }, 
>>>>>>> RAFT-2
  fileFilter: (req, file, cb) => {
    console.log('Multer processing file:', file.originalname, file.mimetype);
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only images are allowed'));
    }
  }
});

// Load proto files
const chatPackageDef = protoLoader.loadSync(path.join(__dirname, 'grpc/chat.proto'));
const chatProto = grpc.loadPackageDefinition(chatPackageDef).chat;

const ttsPackageDef = protoLoader.loadSync(path.join(__dirname, 'grpc/tts.proto'));
const ttsProto = grpc.loadPackageDefinition(ttsPackageDef).tts;

<<<<<<< HEAD
// const authPackageDef = protoLoader.loadSync(path.join(__dirname, 'grpc/auth.proto'));
=======

>>>>>>> RAFT-2
const authPackageDef = protoLoader.loadSync(path.join(__dirname, 'grpc/auth.proto'), {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
  includeDirs: [path.join(__dirname, 'grpc')],
<<<<<<< HEAD
  bytes: Buffer 
=======
  bytes: Buffer  
>>>>>>> RAFT-2
});

const authProto = grpc.loadPackageDefinition(authPackageDef).auth;

// gRPC clients
const chatClient = new chatProto.ChatService(
<<<<<<< HEAD
  'localhost:50052', grpc.credentials.createInsecure()
);

=======
  'localhost:50061', grpc.credentials.createInsecure() 
);


>>>>>>> RAFT-2
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

// Add multer middleware for handling form data
app.use(express.urlencoded({ extended: true }));
<<<<<<< HEAD
=======

// Serve static files
>>>>>>> RAFT-2
app.use(express.static(path.join(__dirname, 'public')));

// Deckard Add, Status Check
// Store user status information
let userPresenceData = [];
const PRESENCE_UPDATE_INTERVAL = 10000; // 10 seconds

// Authentication middleware
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  if (!authHeader) {
    return res.status(401).json({ success: false, message: 'No token provided' });
  }

  const token = authHeader.split(' ')[1];
  if (!token) {
    return res.status(401).json({ success: false, message: 'Invalid token format' });
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
app.post('/api/register', upload.single('avatar'), (req, res) => {
  console.log('Registration request received');
  console.log('Request body:', req.body);
  console.log('Request file:', req.file);
  
<<<<<<< HEAD
  // Convert form data to the format expected by gRPC
=======
 
>>>>>>> RAFT-2
  const registerRequest = {
    username: req.body.username,
    email: req.body.email,
    password: req.body.password,
    full_name: req.body.full_name,
    avatar_url: req.body.avatar_url
  };

<<<<<<< HEAD
  // If there's an avatar file, add it to the request
=======
  
>>>>>>> RAFT-2
  if (req.file) {
    console.log('Processing avatar file:', {
      originalname: req.file.originalname,
      mimetype: req.file.mimetype,
      size: req.file.buffer.length
    });
<<<<<<< HEAD
    // Convert the buffer to a proper Buffer object
=======
    
>>>>>>> RAFT-2
    registerRequest.avatar_data = req.file.buffer;
  }
  
  console.log('Converted register request:', {
    ...registerRequest,
    avatar_data: registerRequest.avatar_data ? `Buffer of size ${registerRequest.avatar_data.length}` : 'None'
  });
  
  authClient.Register(registerRequest, (err, response) => {
    if (err) {
      console.error('gRPC Register error:', err);
      return res.status(500).json({ success: false, message: err.message });
    }
    console.log('Registration response received from gRPC:', response.success);
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

// Protected routes that require authentication
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

// Avatar upload endpoint
app.post('/api/upload-avatar', (req, res, next) => {
  console.log('Received request to /api/upload-avatar');
  console.log('Headers:', req.headers);
  next();
}, authenticateToken, upload.single('image'), (req, res) => {
  console.log('Avatar upload request received from authenticated user:', req.user);
  
  if (!req.file) {
    console.error('No file found in the request. Form fields:', req.body);
    return res.status(400).json({ success: false, message: 'No image file provided' });
  }

  console.log('File received successfully:', {
    originalname: req.file.originalname,
    mimetype: req.file.mimetype,
    size: req.file.buffer.length,
    buffer: req.file.buffer.length > 0 ? 'Contains data' : 'Empty buffer'
  });

  // If this is a registration request, just return the file data
  if (!req.headers['authorization']) {
    return res.json({
      success: true,
      message: 'Avatar received for registration',
      file: {
        buffer: req.file.buffer,
        mimetype: req.file.mimetype
      }
    });
  }

  // For authenticated users, proceed with the gRPC call
  const token = req.headers['authorization'].split(' ')[1];
  authClient.VerifyToken({ token }, (err, response) => {
    if (err || !response.success) {
      return res.status(401).json({ success: false, message: 'Invalid token' });
    }

    const username = response.username;
    console.log('Avatar upload request received from authenticated user:', username);

    authClient.UploadAvatar({
      username: username,
      token: token,
      image_data: Buffer.from(req.file.buffer)
    }, (err, response) => {
      console.log('👉 UploadAvatar sending image_data length:', req.file.buffer.length);
      console.log("🧪 Type of image_data:", Buffer.isBuffer(req.file.buffer));

      if (err) {
        console.error('gRPC UploadAvatar error:', err);
        return res.status(500).json({ success: false, message: err.message });
      }
      console.log('Avatar upload response from gRPC:', response);
      res.json(response);
    });
  });
});

<<<<<<< HEAD
// Avatar retrieval
=======
// Avatar retrieval endpoint
>>>>>>> RAFT-2
app.get('/api/avatar/:username', (req, res) => {
  console.log('Avatar request received for username:', req.params.username);
  
  // Get token from query parameters or authorization header
  const token = req.query.token || (req.headers['authorization'] ? req.headers['authorization'].split(' ')[1] : null);
  
  if (!token) {
    console.log('No token provided for avatar request');
    return res.status(401).json({ success: false, message: 'No token provided' });
  }

  console.log('Calling GetAvatar gRPC with token');
  authClient.GetAvatar({
    username: req.params.username,
    token: token
  }, (err, response) => {
    if (err) {
      console.error('GetAvatar gRPC error:', err);
      return res.status(500).json({ success: false, message: err.message });
    }

    console.log('GetAvatar response:', {
      hasImageData: !!response.image_data,
      hasImageUrl: !!response.image_url,
      success: response.success
    });

    if (response.image_data) {
      console.log('Sending binary image data');
<<<<<<< HEAD
      // If have binary image data, send it directly
=======
      // If we have binary image data, send it directly
>>>>>>> RAFT-2
      res.set('Content-Type', response.image_mimetype || 'image/jpeg');
      res.send(response.image_data);
    } else if (response.image_url) {
      console.log('Redirecting to image URL:', response.image_url);
<<<<<<< HEAD
      // If have a URL, redirect to it
=======
      // If we have a URL, redirect to it
>>>>>>> RAFT-2
      res.redirect(response.image_url);
    } else {
      console.log('No avatar data found, sending default avatar');
      // If no avatar data or URL, send a default avatar
      res.set('Content-Type', 'image/svg+xml');
      res.send(`<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="50" fill="#ddd"/>
        <path d="M50 50m-30 0a30 30 0 1 0 60 0a30 30 0 1 0 -60 0" fill="#fff"/>
      </svg>`);
    }
  });
});

<<<<<<< HEAD
const server = http.createServer(app);
=======
// Create HTTP server
const server = http.createServer(app);

// WebSocket server
>>>>>>> RAFT-2
const wss = new WebSocket.Server({
  server,
  path: '/',
  clientTracking: true,
  perMessageDeflate: {
    zlibDeflateOptions: {
      chunkSize: 1024,
      memLevel: 7,
      level: 3
    },
    zlibInflateOptions: {
      chunkSize: 10 * 1024
    },
    clientNoContextTakeover: true,
    serverNoContextTakeover: true,
    serverMaxWindowBits: 10,
    concurrencyLimit: 10,
    threshold: 1024
  }
});

// Handle server errors
server.on('error', (error) => {
  console.error('Server error:', error);
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught exception:', error);
});

// Store chat history
let chatHistory = [];
let messageIndex = 0; // Add message index tracking

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
    
    // Track which users received the presence data
    const receivingUsers = [];
    clients.forEach((client, username) => {
      if (client.ws && client.ws.readyState === WebSocket.OPEN) {
        client.ws.send(presencePayload);
        receivingUsers.push(username);
      }
    });
    
    console.log(`Broadcasted presence data for ${userPresenceData.length} users to clients: ${receivingUsers.join(', ') || 'none'}`);
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
<<<<<<< HEAD
    console.log(`New client connected: ${username}`);
=======
    console.log(`🧠 New client connected: ${username}`);
>>>>>>> RAFT-2
    
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
<<<<<<< HEAD
      console.log(`Client disconnected: ${username}`);
=======
      console.log(`👋 Client disconnected: ${username}`);
>>>>>>> RAFT-2
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
<<<<<<< HEAD
  console.log("Received from gRPC stream:", msg);
=======
  console.log("📥 Received from gRPC stream:", msg);
>>>>>>> RAFT-2
  
  // Add message to chat history
  chatHistory.push(msg);
  messageIndex++; // Increment message index
  
  // Keep only last 100 messages
  if (chatHistory.length > 100) {
    chatHistory = chatHistory.slice(-100);
  }
  
  // Broadcast text message to all connected clients
  const textPayload = JSON.stringify({ type: 'message', ...msg });
  const messageRecipients = [];
  clients.forEach((client, username) => {
    if (client.ws && client.ws.readyState === WebSocket.OPEN) {
      client.ws.send(textPayload);
      messageRecipients.push(username);
    }
  });
  
<<<<<<< HEAD
  console.log(`Message broadcast to clients: ${messageRecipients.join(', ') || 'none'}`);
=======
  console.log(`📤 Message broadcast to clients: ${messageRecipients.join(', ') || 'none'}`);
>>>>>>> RAFT-2
  
  // Call TTS
  ttsClient.TextToSpeech({ text: msg.message }, (err, response) => {
    if (err) {
      console.error("TTS error:", err);
      return;
    }
    
<<<<<<< HEAD
    console.log("TTS raw response:", response);
    
    if (!response || !response.audioData) {
      console.warn("No audio data received from TTS service.");
=======
    console.log("📦 TTS raw response:", response);
    
    if (!response || !response.audioData) {
      console.warn("⚠️ No audio data received from TTS service.");
>>>>>>> RAFT-2
      return;
    }
    
    // Convert the binary data to base64
    const audioData = Buffer.from(response.audioData).toString('base64');
<<<<<<< HEAD
    console.log("TTS audio data length:", audioData.length);
=======
    console.log("📦 TTS audio data length:", audioData.length);
>>>>>>> RAFT-2
    const audioPayload = JSON.stringify({
      type: 'audio',
      audio: audioData,
      messageIndex: messageIndex - 1  // Use the current message index
    });
    
    const audioRecipients = [];
    clients.forEach((client, username) => {
      if (client.ws && client.ws.readyState === WebSocket.OPEN) {
        client.ws.send(audioPayload);
        audioRecipients.push(username);
      }
    });
    
<<<<<<< HEAD
    console.log(`Audio broadcast to clients: ${audioRecipients.join(', ') || 'none'}`);
=======
    console.log(`🔊 Audio broadcast to clients: ${audioRecipients.join(', ') || 'none'}`);
>>>>>>> RAFT-2
  });
});

// Deckard Add, Status Check
// Cleanup on server shutdown
server.on('close', () => {
  clearInterval(presenceInterval);
  clients.clear();
});

// Start the server
const PORT = process.env.PORT || 8080;
server.listen(PORT, () => {
<<<<<<< HEAD
  console.log(`Server running at http://localhost:${PORT}`);
  console.log(`WebSocket server ready for connections`);
});


// Test Message
=======
  console.log(`🚀 Server running at http://localhost:${PORT}`);
  console.log(`📡 WebSocket server ready for connections`);
});


>>>>>>> RAFT-2
// grpcClient.SendMessage({
//     username: 'test_user',
//     message: 'Hello World!',
//     language: 'en'
//   }, (err, res) => {
//     if (err) console.error("SendMessage error:", err);
//     else console.log("✅ Message sent!");
//   });



  