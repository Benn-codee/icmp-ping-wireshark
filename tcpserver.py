from socket import *

serverPort = 12000

# Membuat socket TCP
serverSocket = socket(AF_INET, SOCK_STREAM)

# Mengikat socket ke port
serverSocket.bind(('', serverPort))

# Server mulai mendengarkan permintaan koneksi (max antrean = 1)
serverSocket.listen(1)

print('Server TCP siap menerima koneksi...')

while True:
    # Menerima koneksi baru dari client (menghasilkan socket baru khusus client tersebut)
    connectionSocket, addr = serverSocket.accept()
    
    # Menerima pesan dari client
    sentence = connectionSocket.recv(1024).decode()
    
    # Memproses data (mengubah ke huruf besar)
    capitalizedSentence = sentence.upper()
    
    # Mengirim balasan ke client
    connectionSocket.send(capitalizedSentence.encode())
    
    # Menutup socket koneksi client
    connectionSocket.close()