from socket import *

serverName = '127.0.0.1'  # IP Server (localhost)
serverPort = 12000

# Membuat socket UDP (AF_INET = IPv4, SOCK_DGRAM = UDP)
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Masukkan kalimat huruf kecil: ')

# Mengirim pesan ke server (harus di-encode ke bytes)
clientSocket.sendto(message.encode(), (serverName, serverPort))

# Menerima balasan dari server
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print('Balasan dari Server:', modifiedMessage.decode())

# Menutup socket
clientSocket.close()