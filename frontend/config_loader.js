const fs = require('fs');
const path = require('path');

function loadConfig() {
    const configPath = path.join(__dirname, '..', 'config', 'frontend_config.json');
    
    try {
        const configData = fs.readFileSync(configPath, 'utf8');
        return JSON.parse(configData);
    } catch (error) {
        console.error('⚠️ Error loading configuration:', error.message);
        console.log('⚠️ Using default configuration');
        return {
            server: {
                port: 8080,
                host: '0.0.0.0'
            },
            services: {
                translation: {
                    host: 'localhost',
                    port: 50051
                },
                chat: {
                    host: 'localhost',
                    port: 50052
                },
                auth: {
                    host: 'localhost',
                    port: 50053
                },
                tts: {
                    host: 'localhost',
                    port: 50054
                }
            }
        };
    }
}

module.exports = { loadConfig }; 