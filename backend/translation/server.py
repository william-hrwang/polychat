from concurrent import futures
import grpc
import translate_pb2
import translate_pb2_grpc
from googletrans import Translator

class TranslationService(translate_pb2_grpc.TranslationServiceServicer):
    def __init__(self):
        self.translator = Translator()

    def TranslateText(self, request, context):
        translated = self.translator.translate(request.text, dest=request.target_lang)
        return translate_pb2.TranslateReply(translated_text=translated.text)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    translate_pb2_grpc.add_TranslationServiceServicer_to_server(TranslationService(), server)
<<<<<<< HEAD
    server.add_insecure_port('[::]:50051')
    server.start()
    print("TranslationService started on [::]:50051") 
=======
    server.add_insecure_port('[::]:50052')
    server.start()
    print("✅ TranslationService started on [::]:50052") 
>>>>>>> RAFT-2
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
