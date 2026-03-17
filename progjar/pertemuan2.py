import socket, sys

# Membuat socket TCP/IP
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Add SO_REUSEADDR untuk memungkinkan penggunaan kembali alamat yang sama
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Mengikat socket ke alamat dan port (localhost:5000)
server_sock.bind(('localhost', 5000))

# Mendengarkan koneksi masuk
server_sock.listen(1)

try:
    while True:
        client_sock, client_addr = server_sock.accept()
        data = client_sock.recv(65535)
        client_sock.send(b'Hello, Client!')
        client_sock.close()
except KeyboardInterrupt:
    print('Server is shutting down.')
    server_sock.close()
    sys.exit(0)