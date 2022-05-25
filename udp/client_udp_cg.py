import socket, sys
import os
import time
import tqdm

#msgFromClient = "Hello UDP Server"

filename = sys.argv[1]
filesize  = os.path.getsize(filename)
host = "192.168.100.102"
port = 5001
SEPARATOR = "<SEPARATOR>"
blocos =0 
buffer_length = int(sys.argv[2])
 
# socket udp do cliente
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPClientSocket.sendto(f"{filename}{SEPARATOR}{filesize}".encode(),(host,port))
#blocos += 1

f = open(filename, "rb")

data = f.read(buffer_length)

progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

while True:
    
    if UDPClientSocket.sendto(data, (host, port)):
        data = f.read(buffer_length)
        #time.sleep(0.01)  # 0.01 segundos
    else:
        break
    blocos += 1
    progress.update(len(data))
UDPClientSocket.close()
f.close()
print(f"Blocos enviados: {blocos}")

