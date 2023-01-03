import socket
import time
import os

host = os.getenv("DB_HOST")
port = int(os.getenv("DB_PORT", default=5432))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((host, port))
        s.close()
        break
    except socket.error as ex:
        time.sleep(0.5)
