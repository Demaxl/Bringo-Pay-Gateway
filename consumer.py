import asyncio
import websockets
import json

from modem import send_ussd_command
from utils import log_message


# WEBSOCKET_USERNAME = os.environ.get('WEBSOCKET_USERNAME')
# WEBSOCKET_PASSWORD = os.environ.get('WEBSOCKET_PASSWORD')
# WEBSOCKET_URL = f"wss://bringopay.xdigt.com/ws/transaction/?username={
#     WEBSOCKET_USERNAME}&password={WEBSOCKET_PASSWORD}"

WEBSOCKET_URL = "ws://127.0.0.1:8000/ws/chat/"

with open("carrier_data.json") as json_file:
    CARRIER_DATA = json.load(json_file)


async def handle_message(message):
    """
    Process the message from the cloud server
    """
    log_message(f"Processing message: {message}")

    modem_port = CARRIER_DATA[str(message["carrier_id"])]["modem_port"]
    modem_password = CARRIER_DATA[str(message["carrier_id"])]["modem_password"]
    commands = CARRIER_DATA[str(message["carrier_id"])
                            ]['transaction_type_ids'][str(message["transaction_type_id"])]

    commands = [command.replace('NUMBER', message["mobile_number"]).replace(
        'AMOUNT', str(message["transaction_amount"])).replace('PASSWORD', modem_password) for command in commands]

    await send_ussd_command(
        modem_port, message["mobile_number"], message["transaction_amount"], commands)


async def websocket_client():
    """
    Connect to the WebSocket server and listen for messages
    """
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        print("Connected to WebSocket server")
        # Continuously listen for messages
        while True:
            message = await websocket.recv()
            message = json.loads(message)
            print(f"Message received: {message}")
            # Start processing the message in parallel
            asyncio.create_task(handle_message(message))


if __name__ == "__main__":
    # Run the WebSocket client
    # asyncio.run(websocket_client())
    test = {
        "user_id": 1,
        "carrier_id": 5,
        "transaction_type_id": 1086,
        "transaction_amount": 6,
        "mobile_number": "0998407604"
    }

    asyncio.run(handle_message(test))
