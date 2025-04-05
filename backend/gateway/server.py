import grpc
<<<<<<< HEAD
from concurrent import futures
=======
import asyncio
>>>>>>> RAFT-2
import chat_pb2
import chat_pb2_grpc
import translate_pb2
import translate_pb2_grpc
<<<<<<< HEAD

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def __init__(self):
        self.clients = []
        channel = grpc.insecure_channel('localhost:50051')
        self.translator = translate_pb2_grpc.TranslationServiceStub(channel)

    def SendMessage(self, request, context):
        translation = self.translator.TranslateText(
            translate_pb2.TranslateRequest(
                text=request.message,
                target_lang='en'
            )
        )

        translated_text = translation.translated_text

        for client in self.clients:
            client.write(chat_pb2.ChatMessage(
                username=request.username,
                message=translated_text,
                original=request.message,
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
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("ChatService started on [::]:50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
=======
import raftos
import json
import sys
from concurrent.futures import ThreadPoolExecutor
import logging

# Enable RAFTOS debug logs
logging.basicConfig(level=logging.INFO)

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
            'db_path': f'/tmp/{node_id}/db',
            'election_min_timeout': 1000,
            'election_max_timeout': 2000
        })

        peer_addresses = [f'127.0.0.1:{50060 + peer}' for peer in peers if peer != node_id]
        self_address = f'127.0.0.1:{50060 + node_id}'
        print(f"[Node {self.node_id}] 🚀 Registering with peers: {peer_addresses}")

        self.message_log = raftos.Replicated(name='chat_log')
        self.register_task = raftos.register(self_address, cluster=peer_addresses)

    async def register(self):
        await self.register_task
        print(f"[Node {self.node_id}] ✅ Registered with RAFT cluster")

    async def wait_for_leader(self, retries=10, delay=1):
        for attempt in range(retries):
            leader_coro = raftos.get_leader()
            leader = await leader_coro if asyncio.iscoroutine(leader_coro) else leader_coro
            print(f"[Node {self.node_id}] 🔍 raftos.get_leader() returned: {leader}")
            if leader:
                return leader
            await asyncio.sleep(delay)
        print(f"[Node {self.node_id}] ❌ No leader elected after {retries} retries.")
        return None

    async def translate_text(self, text, lang='en'):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, lambda: self.translator.TranslateText(
            translate_pb2.TranslateRequest(text=text, target_lang=lang)))

    async def SendMessage(self, request, context):
        print(f"📨 Received SendMessage from {request.username} with text: {request.message}")

        leader = await self.wait_for_leader()
        if not leader:
            return chat_pb2.ChatAck(success=False)

        if leader != f'127.0.0.1:{50060 + self.node_id}':
            print(f"[Node {self.node_id}] ❌ Rejected message from {request.username} — not the leader")
            return chat_pb2.ChatAck(success=False)

        try:
            translation_reply = await self.translate_text(request.message, 'en')
            print(f"[Node {self.node_id}] 🧪 Translated text: {translation_reply.translated_text}")
        except Exception as e:
            print(f"[Node {self.node_id}] ❌ Translation failed: {e}")
            return chat_pb2.ChatAck(success=False)

        message = {
            'username': request.username,
            'message': translation_reply.translated_text,
            'original': request.message,
            'language': request.language
        }

        print(f"[Node {self.node_id}] 📇 Appending message: {message['original']}")
        # Retrieve the current log (or initialize as empty list)
        current_log = await self.message_log.get() or []

        # Append the new message
        current_log.append(json.dumps(message))

        # Update the replicated log with the new list
        await self.message_log.set(current_log)

        return chat_pb2.ChatAck(success=True)

    async def StreamMessages(self, request, context):
        print(f"[Node {self.node_id}] 🥵 StreamMessages started for user: {request.username}")

        class Writer:
            def __init__(self,node_id):
                self.queue = []
                self.node_id = node_id
            def write(self, msg):
                print(f"[Node {self.node_id}] 🗳️ Writing to queue: {msg.username}: {msg.message}")
                self.queue.append(msg)

        writer = Writer(self.node_id)

        self.clients.append(writer)

        async def stream_loop():
            last_index = 0
            while True:
                try:
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
                except Exception as e:
                    print(f"[Node {self.node_id}] ❌ Error in stream_loop: {e}")
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
    await chat_service.register()
    chat_pb2_grpc.add_ChatServiceServicer_to_server(chat_service, server)
    server.add_insecure_port(f'[::]:{grpc_port}')
    await server.start()
    print(f"✅ ChatService [Node {node_id}] started on gRPC port {grpc_port}")
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
>>>>>>> RAFT-2
