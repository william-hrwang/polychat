const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const WebSocket = require('ws');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Load proto
const chatPackageDef = protoLoader.loadSync(path.join(__dirname, 'grpc/chat.proto'));
const chatProto = grpc.loadPackageDefinition(chatPackageDef).chat;

// gRPC client
const grpcClient = new chatProto.ChatService(
  'localhost:50052', grpc.credentials.createInsecure()
);

// tts client
const ttsPackageDef = protoLoader.loadSync(path.join(__dirname, 'grpc/tts.proto'));
const ttsProto = grpc.loadPackageDefinition(ttsPackageDef).tts;

const ttsClient = new ttsProto.TTSService(
  'localhost:50054', grpc.credentials.createInsecure()
);


// Connected WebSocket clients
const clients = new Set();

// HTTP server to serve index.html
const server = http.createServer((req, res) => {
  if (req.url === '/') {
    const file = fs.readFileSync(path.join(__dirname, 'public/index.html'));
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(file);
  }
});

// WebSocket server
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
  console.log('🧠 New browser client connected');
  clients.add(ws);

  ws.on('message', (data) => {
    const message = JSON.parse(data);

    grpcClient.SendMessage({
      username: message.username,
      message: message.message,
      language: message.language
    }, (err, res) => {
      if (err) console.error(err);
    });
  });

  ws.on('close', () => {
    clients.delete(ws);
  });
});

// gRPC stream: receive messages and broadcast
const stream = grpcClient.StreamMessages({ username: 'server' });

// stream.on('data', (msg) => {
//     const data = JSON.stringify(msg);
    
//     // 广播文字消息
//     clients.forEach((client) => client.send(data));
  
//     // 请求语音合成
//     ttsClient.TextToSpeech({ text: msg.message }, (err, response) => {
//       if (err) return console.error("TTS error:", err);
  
//       // 广播音频给前端（base64编码）
//       const audioData = response.audio_data.toString('base64');
//       const audioPayload = JSON.stringify({ audio: audioData });
//       clients.forEach((client) => client.send(audioPayload));
//     });
//   });


stream.on('data', (msg) => {
    console.log("📥 Received from gRPC stream:", msg);
  
    // 广播文字消息
    const textPayload = JSON.stringify(msg);
    clients.forEach((client) => client.send(textPayload));
  
    // 调用 TTS
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
        const audioPayload = JSON.stringify({ audio: audioData });
        clients.forEach((client) => client.send(audioPayload));
      });
  });
  

server.listen(8080, () => {
  console.log('🚀 WebSocket + HTTP server running at http://localhost:8080');
});


grpcClient.SendMessage({
    username: 'test_user',
    message: 'Hello World!',
    language: 'en'
  }, (err, res) => {
    if (err) console.error("SendMessage error:", err);
    else console.log("✅ Message sent!");
  });



  