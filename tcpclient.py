from socket import *

serverName = '127.0.0.1'  # IP Server (localhost)
serverPort = 12000

# Membuat socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
clientSocket = socket(AF_INET, SOCK_STREAM)

# Membuka koneksi TCP ke server
clientSocket.connect((serverName, serverPort))

sentence = input('Masukkan kalimat huruf kecil: ')

# Mengirim pesan melalui koneksi TCP yang aktif
clientSocket.send(sentence.encode())

# Menerima balasan dari server
modifiedSentence = clientSocket.recv(1024)

print('Balasan dari Server:', modifiedSentence.decode())

# Menutup socket
clientSocket.close()