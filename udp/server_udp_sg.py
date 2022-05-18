import socket, select
import tqdm

localIP     = "localhost"
localPort   = 5001
bufferSize  = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

received, add = UDPServerSocket.recvfrom(bufferSize)
filename, filesize = received.split(b"<SEPARATOR>")
filename = "teste1.txt"
filesize = int(filesize)

progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)


with open(filename, "wb") as f:
    while True:
        # lê 1024 bytes do socket
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        if not message:
            #se não recebe nada é pq já recebeu tudo
            break
        # escreve no arquivo os bytes recebidos
        f.write(message)
        # atualiza a barra de progresso
        progress.update(len(message))


UDPServerSocket.close()

