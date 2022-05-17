import socket
import tqdm
import os

# endereço ip
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5001

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

# criando socket do server
# TCP socket
s = socket.socket()

# ligando o socket ao endereço local
s.bind((SERVER_HOST, SERVER_PORT))

# (n) n-> número de conexões não aceitas permitidas
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# se existe conexão, aceita
client_socket, address = s.accept()
# se executar é pq o remetente está conectado
print(f"[+] {address} is connected.")

# recebe as informações o arquivo
# recebe usando o socket do client
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
# remove o caminho absoluto
filename = os.path.basename(filename)
#filename = "teste1.txt"

filesize = int(filesize)

# recebe o arquivo do socket e escreve no arquivo
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "wb") as f:
    while True:
        # lê 1024 bytes do socket
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            #se não recebe nada é pq já recebeu tudo
            break
        # escreve no arquivo os bytes recebidos
        f.write(bytes_read)
        # atualiza a barra de progresso
        progress.update(len(bytes_read))

# fecha o socket do client e do server
client_socket.close()
s.close()