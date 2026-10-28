from socket import *

serverPort = 12000

# Membuat socket UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Mengikat (bind) socket ke port server
serverSocket.bind(('', serverPort))

print("Server UDP siap menerima pesan...")

while True:
    # Menerima data dan alamat pengirim
    message, clientAddress = serverSocket.recvfrom(2048)
    
    # Memproses data (mengubah ke huruf besar)
    modifiedMessage = message.decode().upper()
    
    # Mengirim kembali balasan ke client
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)