import grpc
import asyncio
import chat_pb2
import chat_pb2_grpc
import translate_pb2
import translate_pb2_grpc
import raftos
import json
import sys
from concurrent.futures import ThreadPoolExecutor

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self, node_id, peers):
        self.clients = []
        self.node_id = node_id
        self.executor = ThreadPoolExecutor()

        # Translation service (port 50052)
        channel = grpc.insecure_channel('localhost:50052')
        self.translator = translate_pb2_grpc.TranslationServiceStub(channel)

        # RAFT configuration
        raftos.configure({
            'log_path': f'/tmp/{node_id}/',
            'db_path': f'/tmp/{node_id}/db'
        })

        peer_addresses = [f'127.0.0.1:{50060 + peer}' for peer in peers if peer != node_id]
        self_address = f'127.0.0.1:{50060 + node_id}'
        print(f"[Node {self.node_id}] Registering with peers: {peer_addresses}")

        self.message_log = raftos.Replicated(name='chat_log')
        self.register_task = raftos.register(self_address, cluster=peer_addresses)

    async def translate_text(self, text, lang='en'):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, lambda: 
            self.translator.TranslateText(translate_pb2.TranslateRequest(text=text, target_lang=lang))
        )

    async def SendMessage(self, request, context):
        leader = await raftos.get_leader()
        print(f"[Node {self.node_id}] Current leader: {leader}")

        if leader != f'127.0.0.1:{50060 + self.node_id}':
            print(f"[Node {self.node_id}] ❌ Rejected message from {request.username} — not the leader")
            return chat_pb2.ChatAck(success=False)

        translation_reply = await self.translate_text(request.message, 'en')

        message = {
            'username': request.username,
            'message': translation_reply.translated_text,
            'original': request.message,
            'language': request.language
        }

        print(f"[Node {self.node_id}] Appending message: {message['original']}")
        await self.message_log.append(json.dumps(message))
        return chat_pb2.ChatAck(success=True)

    async def StreamMessages(self, request, context):
        class Writer:
            def __init__(self):
                self.queue = []
            def write(self, msg):
                self.queue.append(msg)

        writer = Writer()
        self.clients.append(writer)

        async def stream_loop():
            last_index = 0
            while True:
                log = await self.message_log.get()
                if log and len(log) > last_index:
                    for i in range(last_index, len(log)):
                        msg = json.loads(log[i])
                        writer.write(chat_pb2.ChatMessage(
                            username=msg['username'],
                            message=msg['message'],
                            original=msg['original'],
                            language=msg['language']
                        ))
                    last_index = len(log)
                await asyncio.sleep(1)

        asyncio.create_task(stream_loop())

        try:
            while True:
                if writer.queue:
                    yield writer.queue.pop(0)
                await asyncio.sleep(0.1)
        except grpc.RpcError:
            print(f"[Node {self.node_id}] ❗ Client disconnected")
        finally:
            self.clients.remove(writer)


async def serve():
    try:
        node_id = int(sys.argv[1])
        peers = list(map(int, sys.argv[2:]))
    except Exception as e:
        print(f"❌ Invalid command line args: {sys.argv}")
        raise e

    grpc_port = 50060 + node_id
    server = grpc.aio.server()
    chat_service = ChatService(node_id, peers)
    await chat_service.register_task
    chat_pb2_grpc.add_ChatServiceServicer_to_server(chat_service, server)
    server.add_insecure_port(f'[::]:{grpc_port}')
    await server.start()
    print(f"✅ ChatService [Node {node_id}] started on gRPC port {grpc_port}")
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
