from socket import *
import sys

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"')
    sys.exit(2)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(100)

while True:
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    
    try:
        message = tcpCliSock.recv(4096).decode('utf-8', errors='ignore')
        if not message:
            tcpCliSock.close()
            continue

        parts = message.split()
        if len(parts) < 2:
            tcpCliSock.close()
            continue
            
        print(f"\n[REQUEST MASUK] {parts[0]} {parts[1]}")
        
        # Ambil URL dari request peramban
        url = parts[1]
        
        # Bersihkan awalan http:// jika ada
        if "http://" in url:
            temp = url.split("http://")[-1]
        else:
            temp = url
            
        # Pisahkan domain (hostn) dan jalur file (uri_path)
        if "/" in temp:
            hostn = temp[:temp.find("/")]
            uri_path = temp[temp.find("/"):]
        else:
            hostn = temp
            uri_path = "/"
            
        hostn = hostn.strip()
        filename = hostn + uri_path.replace('/', '_')
        if filename.endswith('_'):
            filename = filename[:-1]
            
        print(f"--> Host: '{hostn}' | Path: '{uri_path}' | Cache: '{filename}'")
        
        fileExist = False
        try:
            with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                outputdata = f.readlines()
            fileExist = True
            print("--> Membaca dari cache lokal...")
            tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
            for line in outputdata:
                tcpCliSock.send(line.encode())
        except Exception:
            if not fileExist:
                try:
                    print(f"--> Menghubungkan ke server eksternal '{hostn}'...")
                    c = socket(AF_INET, SOCK_STREAM)
                    c.connect((hostn, 80))
                    
                    proxy_request = f"GET {uri_path} HTTP/1.0\r\nHost: {hostn}\r\nConnection: close\r\n\r\n"
                    c.sendall(proxy_request.encode())
                    
                    buff = b""
                    while True:
                        data = c.recv(4096)
                        if not data:
                            break
                        buff += data
                        
                    print(f"--> Data berhasil diunduh ({len(buff)} bytes). Mengirim ke browser & menyimpan cache...")
                    tcpCliSock.sendall(buff)
                    
                    with open(filename, "wb") as tmpFile:
                        tmpFile.write(buff)
                    c.close()
                    
                except Exception as e:
                    print("--> Gagal mengambil data:", e)
            else:
                tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())
                
    except Exception as ex:
        print("--> Error pada koneksi klien:", ex)
        
    tcpCliSock.close()

tcpSerSock.close()