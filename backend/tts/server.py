from concurrent import futures
import grpc
import tts_pb2
import tts_pb2_grpc
from gtts import gTTS
import io

class TTSService(tts_pb2_grpc.TTSServiceServicer):
    def TextToSpeech(self, request, context):
        tts = gTTS(text=request.text, lang='en')  # 可以接收语言参数扩展
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_bytes = audio_fp.getvalue()
        return tts_pb2.AudioReply(audio_data=audio_bytes)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tts_pb2_grpc.add_TTSServiceServicer_to_server(TTSService(), server)
    server.add_insecure_port('[::]:50054')
    server.start()
    print("🔊 TTSService running at [::]:50054")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
