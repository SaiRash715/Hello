import socket
import threading
import os

HOST = '0.0.0.0'
PORT = 5000
FILE_STORAGE = "server_files"

os.makedirs(FILE_STORAGE, exist_ok=True)

def handle_client(client_socket):
    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                break

            command, *args = request.split()

            if command == "UPLOAD":
                filename = args[0]
                filesize = int(args[1])
                file_path = os.path.join(FILE_STORAGE, filename)

                with open(file_path, "wb") as f:
                    received = 0
                    while received < filesize:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        f.write(data)
                        received += len(data)

                client_socket.send(b"UPLOAD_SUCCESS")

            elif command == "DOWNLOAD":
                filename = args[0]
                file_path = os.path.join(FILE_STORAGE, filename)

                if os.path.exists(file_path):
                    filesize = os.path.getsize(file_path)
                    client_socket.send(f"SIZE {filesize}".encode())

                    with open(file_path, "rb") as f:
                        while chunk := f.read(1024):
                            client_socket.send(chunk)
                else:
                    client_socket.send(b"ERROR_FILE_NOT_FOUND")

            elif command == "LIST":
                files = os.listdir(FILE_STORAGE)
                client_socket.send("\n".join(files).encode())

            elif command == "EXIT":
                break

        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"New connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
