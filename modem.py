import serial
import time
import asyncio
from utils import log_message


# Configuration
BAUD_RATE = 115200  # Baud rate


async def send_ussd_command(port, mobile_number, transaction_amount, commands):
    """
    Send a USSD command to the modem and read the response asynchronously.
    """
    try:
        # Create a loop to run in a separate thread
        loop = asyncio.get_event_loop()

        with serial.Serial(port, BAUD_RATE, timeout=5, rtscts=False) as ser:
            ser.flushInput()  # Clear input buffer
            ser.flushOutput()  # Clear output buffer

            for ussd_command in commands:
                # Send the USSD command
                ser.write((ussd_command + '\r').encode())
                log_message(f"Sent: {ussd_command}")

                # Wait for response with timeout using asyncio
                max_wait = 30  # Maximum wait time in seconds
                start_time = time.time()

                while time.time() - start_time < max_wait:
                    if ser.in_waiting:
                        response = ser.read(ser.in_waiting).decode()
                        if response:
                            log_message(f"Received: {response.strip()}")
                            break
                    # Use asyncio.sleep instead of time.sleep
                    await asyncio.sleep(0.1)
                else:
                    log_message("Timeout: No response received.")

    except serial.SerialException as e:
        log_message(f"Error: {e}")
