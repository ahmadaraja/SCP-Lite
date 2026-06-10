# SCP-Lite Protocol Design

## 1. Protocol Name

SCP-Lite stands for Secure Communication Protocol - Lite.

It is a simple educational secure communication protocol designed to demonstrate encrypted communication between a client and a server.

---

## 2. Protocol Requirements

The protocol is designed to meet the following requirements:

1. Establish a TCP connection between a client and a server.
2. Generate an RSA key pair on the server side.
3. Send the server public key to the client.
4. Generate a symmetric AES session key on the client side.
5. Encrypt the AES session key using RSA-OAEP.
6. Send the encrypted AES session key to the server.
7. Authenticate the client using a pre-shared authentication token.
8. Encrypt messages using AES-GCM.
9. Protect message integrity using AES-GCM authentication.
10. Use length-prefixed message framing to transfer data reliably.

---

## 3. Security Goals

### 3.1 Confidentiality

Messages are encrypted using AES-GCM. This prevents unauthorized users from reading the original plaintext message.

### 3.2 Integrity

AES-GCM provides integrity protection. If the ciphertext is modified during transmission, decryption will fail.

### 3.3 Secure Key Exchange

The AES session key is encrypted using RSA-OAEP before being sent to the server. This prevents the session key from being exposed during transmission.

### 3.4 Client Authentication

The client sends a pre-shared authentication token encrypted using AES-GCM. The server decrypts the token and verifies it before accepting the communication session.

### 3.5 Replay Resistance Foundation

Each encrypted message uses a fresh random nonce. This helps prevent repeated ciphertext patterns and provides a foundation for replay resistance.

### 3.6 Reliable Data Framing

The protocol uses a 4-byte length prefix before each message. This allows the receiver to know exactly how many bytes must be read from the TCP stream.

---

## 4. Cryptographic Algorithms

| Purpose               | Algorithm                  |
| --------------------- | -------------------------- |
| Asymmetric Encryption | RSA-OAEP                   |
| RSA Key Size          | 2048-bit                   |
| OAEP Hash Function    | SHA-256                    |
| Symmetric Encryption  | AES-GCM                    |
| AES Key Size          | 128-bit                    |
| Nonce Size            | 12 bytes                   |
| Message Framing       | 4-byte length prefix       |
| Authentication        | Pre-shared encrypted token |

---

## 5. Protocol Message Flow

### Step 1: Server Initialization

The server starts listening on `127.0.0.1:9999`.

The server generates:

* RSA private key
* RSA public key

### Step 2: Client Connection

The client establishes a TCP connection with the server.

### Step 3: Server Public Key Transfer

The server sends its RSA public key to the client in PEM format.

### Step 4: AES Session Key Generation

The client generates a random AES-GCM session key.

### Step 5: Secure Session Key Exchange

The client encrypts the AES session key using the server RSA public key with RSA-OAEP.

The encrypted session key is sent to the server.

### Step 6: Session Key Decryption

The server decrypts the encrypted AES session key using its RSA private key.

At this point, both the client and the server share the same AES session key.

### Step 7: Client Authentication

The client encrypts a pre-shared authentication token using AES-GCM and sends it to the server.

The server decrypts the token and compares it with the expected value.

If the token is correct, the server accepts the client.

If the token is incorrect, the server closes the connection.

### Step 8: Secure Message Transfer

The client encrypts the message using AES-GCM.

The client sends:

1. Nonce
2. Ciphertext

The server decrypts the message using the AES session key.

### Step 9: Secure Server Response

The server encrypts its response using AES-GCM.

The server sends:

1. Response nonce
2. Response ciphertext

The client decrypts the response using the same AES session key.

---

## 6. Message Format

The protocol uses length-prefixed messages over TCP.

Each transmitted data block has the following format:

```text
[4-byte length][data bytes]
```

The first 4 bytes represent the length of the data in big-endian format.

This message framing method helps the receiver know exactly how many bytes must be read from the TCP stream.

---

## 7. Authentication Mechanism

The protocol includes a simple authentication mechanism based on a pre-shared authentication token.

After the AES session key is securely exchanged using RSA-OAEP, the client encrypts the authentication token using AES-GCM and sends it to the server.

The server decrypts the token and verifies its value.

This provides basic client authentication suitable for an educational prototype.

---

## 8. Digital Certificates

The current implementation does not use digital certificates.

The server sends its public key directly to the client. In real-world secure protocols, a digital certificate is used to prove that the public key belongs to a trusted server.

Certificates are usually signed by a trusted Certificate Authority.

Certificate-based authentication is considered a future improvement for this project.

---

## 9. Limitations

This protocol is an educational prototype.

It does not currently include:

* Digital certificates
* Certificate Authority validation
* Mutual authentication
* Multi-client support
* Persistent key storage
* Timestamp-based replay protection
* Production-level network hardening

---

## 10. Future Improvements

The protocol can be improved by adding:

1. Digital certificates.
2. Server certificate verification.
3. Mutual authentication.
4. Timestamp-based replay protection.
5. Multi-client support.
6. Better error handling.
7. Persistent key storage.
8. Logging system.
9. Graphical user interface.

---

## 11. Conclusion

SCP-Lite demonstrates the basic structure of a secure communication protocol.

It combines RSA-OAEP for secure session key exchange, AES-GCM for encrypted communication, and a pre-shared token for basic client authentication.

The project satisfies the educational goal of designing and implementing a secure communication protocol.
