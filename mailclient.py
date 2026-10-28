from socket import *

msg = "\r\n Ini adalah pesan uji coba pengiriman email."
endmsg = "\r\n.\r\n"

mailServer = "localhost" # Ganti dengan alamat mail server tujuan
serverPort = 1025

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, serverPort))

recv = clientSocket.recv(1024).decode()
print(recv)

# Kirim perintah HELO
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
print(clientSocket.recv(1024).decode())

# Kirim perintah MAIL FROM
mailFrom = 'MAIL FROM: <sender@example.com>\r\n'
clientSocket.send(mailFrom.encode())
print(clientSocket.recv(1024).decode())

# Kirim perintah RCPT TO
rcptTo = 'RCPT TO: <recipient@example.com>\r\n'
clientSocket.send(rcptTo.encode())
print(clientSocket.recv(1024).decode())

# Kirim perintah DATA
data = 'DATA\r\n'
clientSocket.send(data.encode())
print(clientSocket.recv(1024).decode())

# Kirim isi pesan
clientSocket.send(msg.encode())
clientSocket.send(endmsg.encode())
print(clientSocket.recv(1024).decode())

# Kirim perintah QUIT
quitCmd = 'QUIT\r\n'
clientSocket.send(quitCmd.encode())
print(clientSocket.recv(1024).decode())

clientSocket.close()