import grpc
from concurrent import futures
import chat_pb2
import chat_pb2_grpc
import translate_pb2
import translate_pb2_grpc
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_loader import load_config

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.clients = []
        channel = grpc.insecure_channel('localhost:50051')
        self.translator = translate_pb2_grpc.TranslationServiceStub(channel)

    def SendMessage(self, request, context):
        translation = self.translator.TranslateText(
            translate_pb2.TranslateRequest(
                text=request.message,
                target_lang='en'  # 后续可以动态改
            )
        )

        translated_text = translation.translated_text

        for client in self.clients:
            client.write(chat_pb2.ChatMessage(
                username=request.username,
                message=translated_text,
                original=request.message,  # 👈 新增原文字段
                language=request.language
            ))
        return chat_pb2.ChatAck(success=True)

    def StreamMessages(self, request, context):
        class Writer:
            def __init__(self):
                self.queue = []
            def write(self, msg):
                self.queue.append(msg)
        writer = Writer()
        self.clients.append(writer)
        while True:
            if writer.queue:
                yield writer.queue.pop(0)


def serve():
    config = load_config('chat')
    if not config:
        print("❌ Failed to load configuration. Using default port 50052")
        port = 50052
        host = '0.0.0.0'
    else:
        port = config['port']
        host = config['host']
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    print(f"✅ ChatService started on {host}:{port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()