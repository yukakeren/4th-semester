import socket
import logging
import hashlib

logging.basicConfig(level=logging.INFO)

HOST = "127.0.0.1"   # lebih jelas daripada 'localhost'
PORT = 5000

def md5_hex(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()

def handle_client(connection: socket.socket, client_address):
    logging.info(f"Connection from {client_address}")
    try:
        data = connection.recv(1024)
        if not data:
            logging.info("Client sent no data (connection closed).")
            return

        decoded = data.decode("utf-8", errors="replace").strip()

        if "|" not in decoded:
            logging.error("Received data is not in the expected 'message|hash' format.")
            return

        # split sekali aja biar message boleh mengandung '|'
        message, received_hash = decoded.rsplit("|", 1)

        calculated_hash = md5_hex(message)

        logging.info(f"Received message: {message}")
        logging.info(f"Received hash: {received_hash}")
        logging.info(f"Calculated hash: {calculated_hash}")

        if calculated_hash == received_hash:
            logging.info("hash valid")
        else:
            logging.warning("hash invalid")

        response = f"{message}|{md5_hex(message)}"
        connection.sendall(response.encode("utf-8"))

    except Exception as e:
        logging.exception(f"Error while handling client {client_address}: {e}")
    finally:
        connection.close()
        logging.info(f"Closed connection {client_address}")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sock.bind((HOST, PORT))
        sock.listen(5)
        logging.info(f"Starting server on {HOST}:{PORT}")

        while True:
            logging.info("Waiting for a connection...")
            connection, client_address = sock.accept()
            handle_client(connection, client_address)

    except KeyboardInterrupt:
        logging.info("Server interrupted by user (Ctrl+C).")
    except Exception as e:
        logging.exception(f"An error occurred: {e}")
    finally:
        logging.info("Shutting down the server.")
        sock.close()

if __name__ == "__main__":
    main()