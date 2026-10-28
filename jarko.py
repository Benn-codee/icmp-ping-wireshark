from socket import *
import sys

# Port server (gunakan selain 80 jika sudah ada web server di host ini)
serverPort = 6789

# Buat TCP welcoming socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Bind ke semua interface supaya bisa diakses dari host lain
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print(f"Server siap di port {serverPort}. Menunggu koneksi...")

# (i) Terima koneksi dari client (browser) -> connection socket
connectionSocket, addr = serverSocket.accept()
print(f"Koneksi dari {addr}")

try:
    # (ii) Terima HTTP request
    message = connectionSocket.recv(4096).decode()
    print("=== Request ===")
    print(message)

    # (iii) Parse request untuk mengetahui file yang diminta
    # Contoh baris pertama: "GET /HelloWorld.html HTTP/1.1"
    filename = message.split()[1]          # "/HelloWorld.html"
    filepath = filename[1:]                # "HelloWorld.html"

    # (iv) Ambil file dari file system server
    with open(filepath, 'rb') as f:
        body = f.read()

    # (v) Buat HTTP response: header + isi file
    header = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode()

    # (vi) Kirim response lewat koneksi TCP
    connectionSocket.sendall(header + body)

except IOError:
    # File tidak ditemukan -> 404 Not Found
    body = b"<html><head><title>404 Not Found</title></head>" \
           b"<body><h1>404 Not Found</h1></body></html>"
    header = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode()
    connectionSocket.sendall(header + body)

except IndexError:
    # Request kosong / tidak valid
    pass

finally:
    connectionSocket.close()
    serverSocket.close()
    sys.exit()
from socket import *
import sys

# Port server (gunakan selain 80 jika sudah ada web server di host ini)
serverPort = 6789

# Buat TCP welcoming socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Bind ke semua interface supaya bisa diakses dari host lain
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print(f"Server siap di port {serverPort}. Menunggu koneksi...")

# (i) Terima koneksi dari client (browser) -> connection socket
connectionSocket, addr = serverSocket.accept()
print(f"Koneksi dari {addr}")

try:
    # (ii) Terima HTTP request
    message = connectionSocket.recv(4096).decode()
    print("=== Request ===")
    print(message)

    # (iii) Parse request untuk mengetahui file yang diminta
    # Contoh baris pertama: "GET /HelloWorld.html HTTP/1.1"
    filename = message.split()[1]          # "/HelloWorld.html"
    filepath = filename[1:]                # "HelloWorld.html"

    # (iv) Ambil file dari file system server
    with open(filepath, 'rb') as f:
        body = f.read()

    # (v) Buat HTTP response: header + isi file
    header = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode()

    # (vi) Kirim response lewat koneksi TCP
    connectionSocket.sendall(header + body)

except IOError:
    # File tidak ditemukan -> 404 Not Found
    body = b"<html><head><title>404 Not Found</title></head>" \
           b"<body><h1>404 Not Found</h1></body></html>"
    header = (
        "HTTP/1.1 404 Not Found\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode()
    connectionSocket.sendall(header + body)

except IndexError:
    # Request kosong / tidak valid
    pass

finally:
    connectionSocket.close()
    serverSocket.close()
    sys.exit()