import socket
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

def send_command(command):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    client.send(command.encode())

    if command.startswith("UPLOAD"):
        filename = command.split()[1]
        if not os.path.exists(filename):
            print("File does not exist locally.")
            client.close()
            return

        filesize = os.path.getsize(filename)
        client.send(f"{filesize}".encode())

        with open(filename, "rb") as f:
            while chunk := f.read(1024):
                client.send(chunk)

        response = client.recv(1024).decode()
        print(response)

    elif command.startswith("DOWNLOAD"):
        response = client.recv(1024).decode()

        if response.startswith("SIZE"):
            filesize = int(response.split()[1])
            filename = command.split()[1]

            with open(filename, "wb") as f:
                received = 0
                while received < filesize:
                    data = client.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    received += len(data)

            print(f"{filename} downloaded successfully.")
        else:
            print("File not found on server.")

    elif command.startswith("LIST"):
        response = client.recv(1024).decode()
        print("Server Files:\n", response)

    client.close()

if __name__ == "__main__":
    while True:
        cmd = input("Enter command (UPLOAD filename / DOWNLOAD filename / LIST / EXIT): ")
        if cmd == "EXIT":
            break
        send_command(cmd)
