import socket

from cryptography.hazmat.primitives import serialization

from crypto_utils import (
    generate_rsa_keys,
    decrypt_session_key,
    decrypt_message,
    encrypt_message,
    send_data,
    receive_data
)


HOST = "127.0.0.1"
PORT = 9999

# Simple pre-shared authentication token.
# Both client and server must use the same token.
AUTH_TOKEN = "SCP-Lite-Secret-Token-2026"


def main():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # Allows reusing the same port quickly after closing the server.
    # This helps avoid WinError 10048 during repeated testing.
    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    client_socket = None

    try:
        server.bind((HOST, PORT))
        server.listen(1)

        print(f"[SERVER] Listening on {HOST}:{PORT}...")

        private_key, public_key = generate_rsa_keys()

        print("[SERVER] RSA keys generated.")

        client_socket, client_address = server.accept()

        print(f"[SERVER] Connection received from {client_address}")

        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        send_data(client_socket, public_pem)

        print("[SERVER] Public key sent to client.")

        encrypted_session_key = receive_data(client_socket)

        session_key = decrypt_session_key(
            private_key,
            encrypted_session_key
        )

        print("[SERVER] Session key decrypted.")

        # ---------------------------------------------------------
        # Client Authentication Step
        # ---------------------------------------------------------
        # The client sends an encrypted authentication token.
        # The server decrypts it using the AES session key.
        # If the token is wrong, the connection is closed.
        # ---------------------------------------------------------

        auth_nonce = receive_data(client_socket)
        auth_ciphertext = receive_data(client_socket)

        client_token = decrypt_message(
            session_key,
            auth_nonce,
            auth_ciphertext
        )

        if client_token != AUTH_TOKEN:
            print("[SERVER] Authentication failed. Connection closed.")
            return

        print("[SERVER] Client authenticated successfully.")

        nonce = receive_data(client_socket)

        print("[SERVER] Nonce received.")

        ciphertext = receive_data(client_socket)

        print("[SERVER] Ciphertext received.")

        message = decrypt_message(
            session_key,
            nonce,
            ciphertext
        )

        print(f"[SERVER] Secure message from client: {message}")

        response = input("Enter secure reply to client: ")

        response_nonce, response_ciphertext = encrypt_message(
            session_key,
            response
        )

        send_data(client_socket, response_nonce)
        send_data(client_socket, response_ciphertext)

        print("[SERVER] Secure response sent.")

    except ConnectionError as error:
        print(f"[SERVER] Connection error: {error}")

    except Exception as error:
        print(f"[SERVER] Error: {error}")

    finally:
        if client_socket:
            client_socket.close()

        server.close()

        print("[SERVER] Connection closed.")


if __name__ == "__main__":
    main()