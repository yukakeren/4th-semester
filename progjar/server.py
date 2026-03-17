import socket
import hashlib
import logging

logging.basicConfig(level=logging.INFO)

HOST = "0.0.0.0"
PORT = 5000

def md5_hex(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()

def handle_client(conn, addr):
    logging.info(f"Connected: {addr}")
    buf = b""
    try:
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                return
            buf += chunk

            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)

                if line.endswith(b"\r"):
                    line = line[:-1]

                h = md5_hex(line)
                logging.info(f"msg={line!r} md5={h}")
                conn.sendall((h + "\n").encode("utf-8"))
    finally:
        conn.close()
        logging.info(f"Closed: {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(50)
        logging.info(f"Listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

if __name__ == "__main__":
    main()