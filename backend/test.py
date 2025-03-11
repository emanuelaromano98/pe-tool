import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:8000/ws/status"
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket")
            while True:
                message = await websocket.recv()
                print(f"Received: {message}")
    except Exception as e:
        print(f"WebSocket connection failed: {e}")

asyncio.run(test_websocket())
