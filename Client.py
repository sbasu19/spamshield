import socket
import threading
import sys

DEFAULT_SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5002

def listen(s):
    while True:
        try:
            data = s.recv(1024)
            if not data:
                print("\n[Disconnected from server]")
                break
            print(f"\n{data.decode()}")
        except:
            break
    s.close()
    sys.exit()

def start_client():
    server_host = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SERVER_HOST

    s = socket.socket()
    try:
        s.connect((server_host, SERVER_PORT))
    except Exception as e:
        print(f"Could not connect to server: {e}")
        return

    print(f"Connected to server at {server_host}:{SERVER_PORT}")
    name = input('Name: ')
    s.send(name.encode()) # Send name first

    t = threading.Thread(target=listen, args=(s,))
    t.daemon = True
    t.start()

    print("Type your message and press Enter (or 'q' to quit):")
    while True:
        try:
            msg = input()
            if not msg:
                continue
            if msg.lower() == 'q':
                break
            s.send(msg.encode()) # Send raw message
        except EOFError:
            break
    s.close()

if __name__ == "__main__":
    start_client()
