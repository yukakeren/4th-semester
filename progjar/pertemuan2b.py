import socket

# Membuat socket TCP/IP
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Menghubungkan ke server di localhost:5000
client_sock.connect(('localhost', 5000))

# Mengirim pesan ke server
# Fungsi b digunakan untuk mengubah string menjadi bytes sebelum dikirim
client_sock.send(b'Hello, Server!')

# Menerima data dari server (jika ada)
# 65535 adalah ukuran buffer untuk menerima data, bisa disesuaikan dengan kebutuhan
data = client_sock.recv(65535)

print('Received from server:', data.decode())  # Mengubah bytes kembali ke string dan mencetaknya

# Menutup koneksi
client_sock.close()
