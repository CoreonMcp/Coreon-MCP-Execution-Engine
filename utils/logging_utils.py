import datetime
import os


def log_trace(message: str, log_file: str = "./logs/mcp_trace.log"):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as f:
        f.write(timestamp + '\t' + message + '\n\n')
