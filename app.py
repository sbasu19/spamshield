from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import socket
import threading
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# Use 'threading' mode to avoid eventlet/gevent complexity and errors
socketio = SocketIO(app, async_mode='threading')

# Map of Socket.IO session IDs to TCP socket connections to Chat_Server.py
tcp_connections = {}

def tcp_listen_thread(sid, tcp_socket):
    """Listens for data from Chat_Server.py and sends it to the browser."""
    while True:
        try:
            data = tcp_socket.recv(1024)
            if not data:
                break
            msg = data.decode()
            # Push message back to the specific browser session
            socketio.emit('new_message', {'msg': msg}, room=sid)
        except:
            break
    
    # Cleanup on disconnect
    if sid in tcp_connections:
        try:
            tcp_connections[sid].close()
        except:
            pass
        del tcp_connections[sid]
    socketio.emit('status', {'msg': '[Disconnected from Server]'}, room=sid)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data.get('username', 'Anonymous')
    sid = request.sid
    
    try:
        # Connect to Chat_Server.py
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(('127.0.0.1', 5002))
        tcp_socket.send(username.encode())
        
        tcp_connections[sid] = tcp_socket
        
        # Start background thread to listen to the TCP server
        t = threading.Thread(target=tcp_listen_thread, args=(sid, tcp_socket))
        t.daemon = True
        t.start()
        
        emit('status', {'msg': f'Connected to SpamShield as {username}'})
    except Exception as e:
        emit('status', {'msg': f'Connection Failed: {str(e)}'})

@socketio.on('send_message')
def handle_message(data):
    sid = request.sid
    msg = data.get('msg', '').strip()
    
    if msg and sid in tcp_connections:
        try:
            tcp_connections[sid].send(msg.encode())
        except Exception as e:
            emit('status', {'msg': f'Send Error: {str(e)}'})

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in tcp_connections:
        tcp_connections[sid].close()
        del tcp_connections[sid]

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
