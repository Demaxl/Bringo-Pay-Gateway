import serial
import time
from .utils import log_message


# Configuration
BAUD_RATE = 115200  # Baud rate


def send_ussd_command(port, mobile_number, transaction_amount, commands):
    """
    Send a USSD command to the modem and read the response.
    """
    ussd_command = f'AT+CUSD=1,"*1000*{mobile_number}*{
        transaction_amount}*2022#"'  # Format command
    try:
        with serial.Serial(port, BAUD_RATE, timeout=5, rtscts=False) as ser:
            ser.flushInput()  # Clear input buffer
            ser.flushOutput()  # Clear output buffer

            # Send the USSD command
            ser.write((ussd_command + '\r').encode())
            log_message(f"Sent: {ussd_command}")

            # Wait for the response
            time.sleep(2)

            # Read response from the modem
            response = ser.read(ser.in_waiting or 1).decode()
            if response:
                log_message(f"Received: {response.strip()}")
            else:
                log_message("No response received.")
    except serial.SerialException as e:
        log_message(f"Error: {e}")
