import os
import sys
import struct
import time
import select
import socket

# Tipe ICMP
ICMP_ECHO_REQUEST = 8

def checksum(string):
    """Menghitung checksum untuk header ICMP"""
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = string[count+1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    """Menerima balasan (Echo Reply) dari server"""
    timeLeft = timeout

    while True:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)

        if whatReady[0] == []: # Timeout
            return "Request timed out."

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Header ICMP berada setelah header IP (20 byte pertama)
        icmpHeader = recPacket[20:28]
        type, code, checksum_val, packetID, sequence = struct.unpack("bbHHh", icmpHeader)

        if packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            rtt = (timeReceived - timeSent) * 1000  # Konversi ke milidetik
            return f"Reply from {addr[0]}: bytes={len(recPacket)-28} RTT={rtt:.2f}ms TTL={recPacket[8]}"

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."

def sendOnePing(mySocket, destAddr, ID):
    """Mengirimkan satu paket ICMP Echo Request"""
    myChecksum = 0

    # Header ICMP: Type (8), Code (0), Checksum (0), ID, Sequence (1)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time()) # Menyimpan timestamp sebagai payload

    # Hitung checksum header + data
    myChecksum = checksum(header + data)

    if sys.platform == 'darwin':
        myChecksum = socket.htons(myChecksum) & 0xffff
    else:
        myChecksum = socket.htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data

    mySocket.sendto(packet, (destAddr, 1))

def doOnePing(destAddr, timeout):
    """Proses pembuatan socket dan eksekusi ping"""
    icmp = socket.getprotobyname("icmp")
    try:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error as e:
        print(f"Socket Error: {e}. Pastikan Anda menjalankan program sebagai Administrator/Root!")
        return

    myID = os.getpid() & 0xFFFF  # ID unik berbasis Process ID
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)

    mySocket.close()
    return delay

def ping(host, timeout=1):
    try:
        dest = socket.gethostbyname(host)
        print(f"Pinging {host} [{dest}] with 32 bytes of data:")
        for i in range(4): # Kirim 4 paket ping
            result = doOnePing(dest, timeout)
            print(result)
            time.sleep(1)
    except socket.gaierror:
        print(f"Cannot resolve host: {host}")

if __name__ == '__main__':
    # Contoh target ping
    target_host = "gaia.cs.umass.edu" # atau "8.8.8.8" / "google.com"
    ping(target_host)