import socket
import threading
import joblib
import re
import pandas as pd
from datetime import datetime

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5002
model = joblib.load('spam_model.pkl')

def extract_features(msg):
    num_links = len(re.findall(r'http[s]?://|www\.|\.com|\.org|\.net', msg.lower()))
    words = msg.split()
    num_words = len(words)
    has_offer = 1 if any(word in msg.lower() for word in ['free', 'win', 'prize', 'cash', 'money', 'offer']) else 0
    sender_score = 0.5  # Default score
    all_caps = 1 if msg.isupper() and len(msg) > 5 else 0
    links_per_word = num_links / num_words if num_words > 0 else 0
    
    features = pd.DataFrame([[num_links, num_words, has_offer, sender_score, all_caps, links_per_word]], 
                           columns=['num_links', 'num_words', 'has_offer', 'sender_score', 'all_caps', 'links_per_word'])
    return features

client_sockets = {} # Map socket to username
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f'Listening on {SERVER_HOST}:{SERVER_PORT}')

def check_spam(msg):
    features = extract_features(msg)
    prediction = model.predict(features)[0]
    return 'SPAM' if prediction == 1 else 'OK'

def listen_for_client(cs):
    try:
        # First message is the username
        username = cs.recv(1024).decode()
        client_sockets[cs] = username
        print(f'{username} connected')
        
        while True:
            data = cs.recv(1024)
            if not data:
                break
            
            msg = data.decode()
            status = check_spam(msg)
            
            if status == 'SPAM':
                cs.send(b'[SPAM BLOCKED]')
                continue
            
            # Format message after spam check
            formatted_msg = f'[{datetime.now().strftime("%H:%M")}] {username}: {msg}'
            
            for client in list(client_sockets.keys()):
                try:
                    client.send(formatted_msg.encode())
                except:
                    if client in client_sockets:
                        del client_sockets[client]
    except Exception as e:
        print(f'Error with client: {e}')
    
    if cs in client_sockets:
        print(f'{client_sockets[cs]} disconnected')
        del client_sockets[cs]
    cs.close()

while True:
    client_socket, addr = s.accept()
    t = threading.Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()
