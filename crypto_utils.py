from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


def generate_rsa_keys():
    """
    Generate RSA private and public keys.
    RSA is used to protect the AES session key during exchange.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    return private_key, public_key


def generate_session_key():
    """
    Generate a 128-bit AES session key.
    This key is used to encrypt secure messages.
    """
    return AESGCM.generate_key(bit_length=128)


def encrypt_message(session_key, plaintext):
    """
    Encrypt a plaintext message using AES-GCM.

    AES-GCM provides:
    - Confidentiality
    - Integrity
    - Authentication of encrypted data
    """
    aesgcm = AESGCM(session_key)

    # AES-GCM recommended nonce size is 12 bytes.
    nonce = os.urandom(12)

    ciphertext = aesgcm.encrypt(
        nonce,
        plaintext.encode(),
        None
    )

    return nonce, ciphertext


def decrypt_message(session_key, nonce, ciphertext):
    """
    Decrypt an AES-GCM encrypted message.
    If the ciphertext is modified, decryption will fail.
    """
    aesgcm = AESGCM(session_key)

    plaintext = aesgcm.decrypt(
        nonce,
        ciphertext,
        None
    )

    return plaintext.decode()


def encrypt_session_key(public_key, session_key):
    """
    Encrypt the AES session key using the server RSA public key.
    RSA-OAEP with SHA-256 is used.
    """
    encrypted_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_key


def decrypt_session_key(private_key, encrypted_key):
    """
    Decrypt the AES session key using the server RSA private key.
    """
    session_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return session_key


def send_data(sock, data):
    """
    Send data with a 4-byte length prefix.
    This helps the receiver know exactly how many bytes to read.
    """
    data_length = len(data)

    sock.sendall(
        data_length.to_bytes(4, "big")
    )

    sock.sendall(data)


def receive_exact(sock, length):
    """
    Receive exactly the required number of bytes.
    Raises ConnectionError if the connection closes early.
    """
    data = b""

    while len(data) < length:
        packet = sock.recv(
            length - len(data)
        )

        if not packet:
            raise ConnectionError("Connection closed before receiving expected data.")

        data += packet

    return data


def receive_data(sock):
    """
    Receive length-prefixed data from the socket.
    """
    length_bytes = receive_exact(sock, 4)

    data_length = int.from_bytes(
        length_bytes,
        "big"
    )

    return receive_exact(sock, data_length)