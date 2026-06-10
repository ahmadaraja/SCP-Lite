from crypto_utils import (
    generate_rsa_keys,
    generate_session_key,
    encrypt_session_key,
    decrypt_session_key,
    encrypt_message,
    decrypt_message
)


AUTH_TOKEN = "SCP-Lite-Secret-Token-2026"


def main():
    private_key, public_key = generate_rsa_keys()

    session_key = generate_session_key()

    encrypted_session_key = encrypt_session_key(
        public_key,
        session_key
    )

    decrypted_session_key = decrypt_session_key(
        private_key,
        encrypted_session_key
    )

    message = "Hello, this is a secure message."

    nonce, ciphertext = encrypt_message(
        decrypted_session_key,
        message
    )

    decrypted_message = decrypt_message(
        decrypted_session_key,
        nonce,
        ciphertext
    )

    auth_nonce, auth_ciphertext = encrypt_message(
        decrypted_session_key,
        AUTH_TOKEN
    )

    decrypted_token = decrypt_message(
        decrypted_session_key,
        auth_nonce,
        auth_ciphertext
    )

    print("Original Message:")
    print(message)

    print("\nEncrypted Message:")
    print(ciphertext)

    print("\nDecrypted Message:")
    print(decrypted_message)

    print("\nOriginal Authentication Token:")
    print(AUTH_TOKEN)

    print("\nDecrypted Authentication Token:")
    print(decrypted_token)

    if (
        session_key == decrypted_session_key
        and message == decrypted_message
        and AUTH_TOKEN == decrypted_token
    ):
        print("\nTest Passed: Encryption, decryption, and authentication token work correctly.")
    else:
        print("\nTest Failed: Something is wrong.")


if __name__ == "__main__":
    main()