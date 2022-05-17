import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

#Endereço ip e porta do server
host = "192.168.3.7"
port = 5001

# arquivo a se enviado
filename = "teste.txt"
# tamanho do arquivo
filesize = os.path.getsize(filename)

# criando o socket do client
s = socket.socket()

print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")

# enviando o nome do arquivo e o tamanho
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

# enviando o arquivo
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    while True:
        # lendo bytes do arquivo
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # se acabou de transmitir os bytes do arquivo
            break
        # sendall para garantir a transmissão
        s.sendall(bytes_read)
        # atualização da barra de progresso
        progress.update(len(bytes_read))
# fecha o socket
s.close()