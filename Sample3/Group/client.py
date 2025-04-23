import socket
import threading

HOST, PORT = '192.168.29.106', 5000

def receive(client):
    while True:
        try:
            print(client.recv(1024).decode())
        except:
            print("Connection closed by server.")
            break

client = socket.socket()

try:
    client.connect((HOST, PORT))
    print("Connected to server.")

    # Start thread for receiving messages
    threading.Thread(target=receive, args=(client,), daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == 'exit':
            break
        client.send(msg.encode())

except Exception as e:
    print(f"Failed to connect: {e}")

finally:
    client.close()
    print("Disconnected.")
