from socket import *
import threading

def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        with open(filename[1:], 'r') as f:
            outputdata = f.read()
        
        # Kirim HTTP response header
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        
        # Kirim isi file ke klien
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
    except IOError:
        # Kirim response 404 jika file tidak ditemukan
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
    finally:
        connectionSocket.close()

def start_server():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', 6789))
    serverSocket.listen(5)
    print('Web Server siap beroperasi pada port 6789...')
    
    while True:
        connectionSocket, addr = serverSocket.accept()
        threading.Thread(target=handle_client, args=(connectionSocket,)).start()

if __name__ == '__main__':
    start_server()