import socket

from cryptography.hazmat.primitives import serialization

from crypto_utils import (
    generate_session_key,
    encrypt_session_key,
    encrypt_message,
    decrypt_message,
    send_data,
    receive_data
)


HOST = "127.0.0.1"
PORT = 9999

# Simple pre-shared authentication token.
# It must match the token stored on the server.
AUTH_TOKEN = "SCP-Lite-Secret-Token-2026"


def main():
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        client.connect((HOST, PORT))

        print(f"[CLIENT] Connected to server {HOST}:{PORT}")

        public_pem = receive_data(client)

        server_public_key = serialization.load_pem_public_key(
            public_pem
        )

        print("[CLIENT] Server public key received.")

        session_key = generate_session_key()

        print("[CLIENT] AES session key generated.")

        encrypted_session_key = encrypt_session_key(
            server_public_key,
            session_key
        )

        send_data(client, encrypted_session_key)

        print("[CLIENT] Encrypted session key sent.")

        # ---------------------------------------------------------
        # Client Authentication Step
        # ---------------------------------------------------------
        # The authentication token is encrypted using AES-GCM.
        # This proves that the client knows the shared secret token.
        # ---------------------------------------------------------

        auth_nonce, auth_ciphertext = encrypt_message(
            session_key,
            AUTH_TOKEN
        )

        send_data(client, auth_nonce)
        send_data(client, auth_ciphertext)

        print("[CLIENT] Authentication token sent securely.")

        message = input("Enter a secure message: ")

        nonce, ciphertext = encrypt_message(
            session_key,
            message
        )

        print("[CLIENT] Message encrypted.")

        send_data(client, nonce)
        send_data(client, ciphertext)

        print("[CLIENT] Secure message sent.")

        response_nonce = receive_data(client)
        response_ciphertext = receive_data(client)

        response_message = decrypt_message(
            session_key,
            response_nonce,
            response_ciphertext
        )

        print(f"[CLIENT] Secure response from server: {response_message}")

    except ConnectionRefusedError:
        print("[CLIENT] Connection refused. Make sure the server is running first.")

    except ConnectionError as error:
        print(f"[CLIENT] Connection error: {error}")

    except Exception as error:
        print(f"[CLIENT] Error: {error}")

    finally:
        client.close()

        print("[CLIENT] Connection closed.")


if __name__ == "__main__":
    main()