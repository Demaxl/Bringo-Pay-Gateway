"""
Example request:
{
    user_id: 1,
    carrier_id: 6,
    transaction_type_id: 2
    transaction_amount: 5
    mobile_number: 0998407604 
}
"""
import os
import asyncio
import websockets

from .utils import log_message


# WEBSOCKET_USERNAME = os.environ.get('WEBSOCKET_USERNAME')
# WEBSOCKET_PASSWORD = os.environ.get('WEBSOCKET_PASSWORD')
# WEBSOCKET_URL = f"wss://bringopay.xdigt.com/ws/transaction/?username={
#     WEBSOCKET_USERNAME}&password={WEBSOCKET_PASSWORD}"

WEBSOCKET_URL = "ws://127.0.0.1:8000/ws/chat/"


async def handle_message(message):
    """
    Process the message from the cloud server
    """
    # log_message(f"Processing message: {message['message']}")
    log_message(f"Processing message: {message}")
    await asyncio.sleep(1)
    print(f"Finished processing: {message}")


async def websocket_client():
    """
    Connect to the WebSocket server and listen for messages
    """
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        print("Connected to WebSocket server")
        # Continuously listen for messages
        while True:
            message = await websocket.recv()
            print(f"Message received: {message}")
            # Start processing the message in parallel
            asyncio.create_task(handle_message(message))

# Run the WebSocket client
asyncio.run(websocket_client())
