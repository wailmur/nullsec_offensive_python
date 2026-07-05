import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 1234

client_sock = socket.socket() # default is TCP
client_sock.connect((SERVER_IP, SERVER_PORT))
client_sock.sendall("HELLO WORLD!".encode())
print("DATA SENT.")

client_sock.close()