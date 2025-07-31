import asyncio
import websockets

async def handle_connection(websocket, path):
    print("🔌 Client connected...")
    async for message in websocket:
        print("📡 Audio packet received (bytes):", len(message))

start_server = websockets.serve(handle_connection, "0.0.0.0", 8765)

print("🚀 WebSocket server running on ws://localhost:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
