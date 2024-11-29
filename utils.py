import datetime


LOG_FILE = 'websocket_transaction.log'


def log_message(message):
    """
    Log messages to a file with timestamps.
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    log_entry = f"[{timestamp}] {message}"
    with open(LOG_FILE, 'a') as log:
        log.write(log_entry + '\n')
    print(log_entry, flush=True)
