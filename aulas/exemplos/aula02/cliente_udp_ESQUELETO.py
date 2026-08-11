# cliente_udp_ESQUELETO.py — CASA da Aula 2: eco em UDP (cliente)
# Complete os TODOs. Em UDP NAO ha connect(): o endereco vai em cada sendto().
import socket

HOST, PORT = "127.0.0.1", 5001
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # SOCK_DGRAM = UDP
s.settimeout(5)                                        # UDP pode perder: use tempo-limite

mensagem = "oi via UDP"
# TODO 1: envie 'mensagem' (em bytes) para (HOST, PORT) com s.sendto(...)
# TODO 2: receba a resposta com s.recvfrom(1024) e imprima o texto recebido

s.close()
