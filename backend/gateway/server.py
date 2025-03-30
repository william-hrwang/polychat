import grpc
from concurrent import futures
import chat_pb2
import chat_pb2_grpc
import translate_pb2
import translate_pb2_grpc

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.clients = []
        channel = grpc.insecure_channel('localhost:50051')
        self.translator = translate_pb2_grpc.TranslationServiceStub(channel)

    def SendMessage(self, request, context):
        translation = self.translator.TranslateText(
            translate_pb2.TranslateRequest(
                text=request.message,
                target_lang='en'  # For now, fixed
            )
        )
        for client in self.clients:
            client.write(chat_pb2.ChatMessage(
                username=request.username,
                message=translation.translated_text,
                language='en'
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
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("✅ ChatService started on [::]:50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()