import socket
import os
import zipfile

# client configuration
HOST = '192.168.2.18'  # Gizem's (server's) IP address
PORT = 65432  # The same port used by the server
SAVE_PATH = 'D:/'  # Path to save the received files
CHUNK_SIZE = 1024 * 1024  # 1 MB buffer size

if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)
    print(f"Directory {SAVE_PATH} created.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print("Connected to server.")

    while True:  # files to be received one by one
        file_size_data = client_socket.recv(1024).decode()  # receiving file size
        if not file_size_data:
            break  # No more files to receive

        file_size = int(file_size_data)
        print(f"Receiving file of size: {file_size} bytes")

        # change this to rename received files
        received_file_path = os.path.join(SAVE_PATH, "received_file.zip")
        with open(received_file_path, 'wb') as f:
            bytes_received = 0
            while bytes_received < file_size:
                data = client_socket.recv(CHUNK_SIZE)
                if not data:
                    break
                f.write(data)
                bytes_received += len(data)
                print(f"Received {len(data)} bytes, total {bytes_received}/{file_size} bytes")

        print(f"Received and saved zipped file: {received_file_path}")

        # Unzip the file after receiving it
        unzip_dir = os.path.join(SAVE_PATH, 'unzipped_files')
        if not os.path.exists(unzip_dir):
            os.makedirs(unzip_dir)

        with zipfile.ZipFile(received_file_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_dir)
            print(f"Extracted files to {unzip_dir}")

    print("File transfer completed.")
