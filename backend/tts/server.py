from concurrent import futures
import grpc
import tts_pb2
import tts_pb2_grpc
from gtts import gTTS
import io
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSService(tts_pb2_grpc.TTSServiceServicer):
    def TextToSpeech(self, request, context):
        try:
            logger.info(f"Received TTS request for text: {request.text[:50]}...")
            # Create TTS object with specific parameters
            tts = gTTS(
                text=request.text,
                lang='en',
                slow=False,
                tld='com'  # Use US English accent
            )
            
            # Create in-memory file
            audio_fp = io.BytesIO()
            
            # Write to the in-memory file
            tts.write_to_fp(audio_fp)
            
            # Get the bytes
            audio_bytes = audio_fp.getvalue()
            
            # Log the first few bytes to verify format
            logger.info(f"Generated audio data of length: {len(audio_bytes)} bytes")
            logger.info(f"First 20 bytes: {audio_bytes[:20]}")
            
            # Return the audio data
            return tts_pb2.AudioReply(audio_data=audio_bytes)
            
        except Exception as e:
            logger.error(f"Error in TextToSpeech: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return tts_pb2.AudioReply()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tts_pb2_grpc.add_TTSServiceServicer_to_server(TTSService(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    logger.info("🔊 TTSService running at [::]:50054")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
