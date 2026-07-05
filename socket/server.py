import socket

SERVER_IP = '0.0.0.0'
SERVER_PORT = 1234

server_sock = socket.socket() # default is TCP
server_sock.bind((SERVER_IP, SERVER_PORT))
server_sock.listen()
connection, address = server_sock.accept()
data = connection.recv(1024)
print(data.decode('utf-8'))
server_sock.close()