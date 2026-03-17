import socket

HOST = 'a.nafkhan.id'
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024).decode()
    print(data)

    s.sendall('5025241299'.encode())
    data = s.recv(1024).decode()
    print(data)

    s.close()
