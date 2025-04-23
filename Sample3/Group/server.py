import socket
import threading

HOST, PORT = '192.168.29.106', 5000
clients = []

def handle_client(client, addr):
    print(f"[NEW] {addr} connected.")
    while True:
        try:
            msg = client.recv(1024).decode()
            if not msg:
                break
            print(f"[{addr}] {msg}")
            broadcast(f"[{addr}] {msg}", client)
        except:
            break
    clients.remove(client)
    client.close()
    print(f"[DISCONNECT] {addr} disconnected.")

def broadcast(msg, sender):
    for c in clients:
        if c != sender:
            try:
                c.send(msg.encode())
            except:
                clients.remove(c)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTED] Server running on {HOST}:{PORT}")
    
    while True:
        client, addr = server.accept()
        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
