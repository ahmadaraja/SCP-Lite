# SCP-Lite: Secure Communication Protocol

## Project Overview

SCP-Lite is an educational secure client-server communication protocol implemented in Python.

The project demonstrates how a client and a server can establish a protected communication session using:

* RSA-OAEP for secure AES session key exchange
* AES-GCM for encrypted communication
* A pre-shared authentication token for basic client authentication
* Fresh random nonces for encrypted messages
* Length-prefixed message framing over TCP sockets

This project was developed for the Secure Communication Protocols course.

---

## Security Goals

### 1. Confidentiality

Messages are encrypted using AES-GCM, preventing unauthorized parties from reading plaintext messages.

### 2. Integrity

AES-GCM provides authentication and integrity protection. If encrypted data is modified during transmission, decryption fails.

### 3. Secure Session Key Exchange

The client generates an AES session key and encrypts it using the server RSA public key with RSA-OAEP and SHA-256.

### 4. Client Authentication

The client encrypts a pre-shared authentication token using AES-GCM. The server decrypts the token and verifies it before accepting the secure session.

### 5. Reliable Message Framing

The protocol uses a 4-byte length prefix before every transmitted data block. This helps the receiver know exactly how many bytes must be read from the TCP stream.

---

## Technologies Used

* Python 3
* TCP sockets
* cryptography library
* RSA-OAEP
* AES-GCM
* SHA-256
* PyCharm

---

## Project Structure

```text
SCP-Lite/
│
├── client.py
├── server.py
├── crypto_utils.py
├── test_crypto.py
├── protocol.md
├── README.md
├── requirements.txt
├── .gitignore
├── SCP-LiteDiagram.png
```

---

## How the Protocol Works

### Step 1: Server Initialization

The server starts listening on `127.0.0.1:9999` and generates an RSA key pair.

### Step 2: Client Connection

The client establishes a TCP connection with the server.

### Step 3: Public Key Transfer

The server sends its RSA public key to the client in PEM format.

### Step 4: AES Session Key Generation

The client generates a random AES-GCM session key.

### Step 5: Secure Session Key Exchange

The client encrypts the AES session key using the server RSA public key with RSA-OAEP.

The server decrypts the session key using its RSA private key.

At this point, both sides share the same AES session key.

### Step 6: Client Authentication

The client encrypts a pre-shared authentication token using AES-GCM and sends it to the server.

The server decrypts the token and compares it with the expected value.

If the token is correct, the session continues.

If the token is incorrect, the server closes the connection.

### Step 7: Secure Message Transfer

The client encrypts a message using AES-GCM and sends the nonce and ciphertext to the server.

### Step 8: Secure Server Response

The server decrypts the client message, writes a response, encrypts it using AES-GCM, and sends the encrypted response back to the client.

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

Open the first terminal and run:

```bash
python server.py
```

### 3. Run the client

Open a second terminal and run:

```bash
python client.py
```

### 4. Run the crypto test

```bash
python test_crypto.py
```

Expected result:

```text
Test Passed: Encryption, decryption, and authentication token work correctly.
```

---

## Example Output

### Server

```text
[SERVER] Listening on 127.0.0.1:9999...
[SERVER] RSA keys generated.
[SERVER] Connection received from ('127.0.0.1', 50000)
[SERVER] Public key sent to client.
[SERVER] Session key decrypted.
[SERVER] Client authenticated successfully.
[SERVER] Nonce received.
[SERVER] Ciphertext received.
[SERVER] Secure message from client: Hello Server
Enter secure reply to client: Hello Client
[SERVER] Secure response sent.
[SERVER] Connection closed.
```

### Client

```text
[CLIENT] Connected to server 127.0.0.1:9999
[CLIENT] Server public key received.
[CLIENT] AES session key generated.
[CLIENT] Encrypted session key sent.
[CLIENT] Authentication token sent securely.
Enter a secure message: Hello Server
[CLIENT] Message encrypted.
[CLIENT] Secure message sent.
[CLIENT] Secure response from server: Hello Client
[CLIENT] Connection closed.
```

---

## Cryptographic Algorithms

| Purpose               | Algorithm                  |
| --------------------- | -------------------------- |
| Asymmetric Encryption | RSA-OAEP                   |
| RSA Key Size          | 2048-bit                   |
| OAEP Hash Function    | SHA-256                    |
| Symmetric Encryption  | AES-GCM                    |
| AES Key Size          | 128-bit                    |
| Nonce Size            | 12 bytes                   |
| Authentication        | Pre-shared encrypted token |
| Message Framing       | 4-byte length prefix       |

---

## Limitations

This project is an educational prototype and is not intended for production use.

It does not currently include:

* Digital certificates
* Certificate Authority validation
* Mutual authentication
* Multi-client support
* Persistent key storage
* Timestamp-based replay protection
* Production-level security hardening

---

## Future Improvements

The protocol can be improved by adding:

* Digital certificate validation
* Server identity verification
* Mutual authentication
* Multi-client support
* Timestamp-based replay protection
* Better exception handling
* Persistent key storage
* Logging system
* Graphical user interface

---

## Authors

Ahmad Araja
---

## Conclusion

SCP-Lite demonstrates the core design of a secure communication protocol.

It combines RSA-OAEP for secure session key exchange, AES-GCM for encrypted communication, and a pre-shared authentication token for basic client authentication.

The project satisfies the educational goal of designing and implementing a secure communication protocol prototype.
