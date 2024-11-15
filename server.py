import socket
import os

HOST = '0.0.0.0' # best host number for the server
PORT = 65432
FOLDER_PATH = 'C:/Users/Gizem/'  # Path to the folder you want to send
CHUNK_SIZE = 1024 * 1024  # 1 MB buffer size


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server is listening for connections...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")

        for root, dirs, files in os.walk(FOLDER_PATH):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                conn.sendall(f"{file_size}".encode())  # Send the file size b4 files
                with open(file_path, 'rb') as f:
                    while chunk := f.read(CHUNK_SIZE):
                        conn.sendall(chunk)
                print(f"Sent {file_path} - {file_size} bytes")
        print("File transfer completed.")
