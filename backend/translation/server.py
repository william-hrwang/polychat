from concurrent import futures
import grpc
import translate_pb2
import translate_pb2_grpc
from googletrans import Translator
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_loader import load_config

class TranslationService(translate_pb2_grpc.TranslationServiceServicer):
    def __init__(self):
        self.translator = Translator()

    def TranslateText(self, request, context):
        translated = self.translator.translate(request.text, dest=request.target_lang)
        return translate_pb2.TranslateReply(translated_text=translated.text)

def serve():
    config = load_config('translation')
    if not config:
        print("❌ Failed to load configuration. Using default port 50051")
        port = 50051
        host = '0.0.0.0'
    else:
        port = config['port']
        host = config['host']
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    translate_pb2_grpc.add_TranslationServiceServicer_to_server(TranslationService(), server)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    print(f"✅ TranslationService started on {host}:{port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
