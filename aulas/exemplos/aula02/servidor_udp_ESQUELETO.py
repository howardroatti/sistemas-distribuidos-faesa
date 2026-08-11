# servidor_udp_ESQUELETO.py — CASA da Aula 2: eco em UDP (servidor)
# Complete os TODOs. Compare com o servidor_eco.py (TCP): em UDP NAO existe
# listen()/accept() — o socket ja recebe de qualquer cliente com recvfrom().
import socket

HOST, PORT = "127.0.0.1", 5001            # porta diferente do TCP (5000), para nao conflitar

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # SOCK_DGRAM = UDP
s.bind((HOST, PORT))
print(f"[udp] ouvindo em {HOST}:{PORT}", flush=True)

while True:
    dado, endereco = s.recvfrom(1024)     # recebe os bytes E o endereco do remetente
    print(f"[udp] recebi {dado!r} de {endereco}", flush=True)
    # TODO: devolva o MESMO 'dado' de volta para 'endereco' (eco),
    #       usando s.sendto(dado, endereco)
