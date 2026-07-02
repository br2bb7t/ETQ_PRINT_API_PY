import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from application.constants import constants
from infrastructure.logging.LoggerImplements import LoggerImplements

log_impl = LoggerImplements("DecryptLogger")

NONCE_SIZE = 12


class DecryptService:

    @staticmethod
    def decrypt(secret_name: str) -> str:
        """
        Decrypts encrypted text using Azure Key Vault or AES-GCM.
        """

        try:

            log_impl.log_information("Starting decryption process", "decrypt")

            # AES-GCM flow
            if not secret_name:
                return ""

            log_impl.log_information("Using AES-GCM decryption", "decrypt")

            key = base64.b64decode(constants.AES_KEY)

            encrypted_payload = base64.b64decode(secret_name)

            nonce = encrypted_payload[:NONCE_SIZE]
            ciphertext = encrypted_payload[NONCE_SIZE:]

            aesgcm = AESGCM(key)

            plaintext = aesgcm.decrypt(nonce, ciphertext, None)

            return plaintext.decode("utf-8")

        except Exception as e:
            log_impl.log_error(f"Error during decryption: {e}", "decrypt", f"Error: {e}")
            raise RuntimeError("Error retrieving the secret")

    @staticmethod
    def encrypt(plain_text: str) -> str:
        """
        Encrypts plain text using AES-GCM.
        """

        try:

            if not plain_text:
                return ""

            log_impl.log_information("Starting encryption process", "encrypt")

            key = base64.b64decode(constants.AES_KEY)
            nonce = os.urandom(NONCE_SIZE)
            aesgcm = AESGCM(key)

            ciphertext = aesgcm.encrypt(nonce, plain_text.encode("utf-8"), None)
            encrypted_payload = nonce + ciphertext

            encrypted_base64 = base64.b64encode(encrypted_payload).decode("utf-8")

            log_impl.log_information("Encryption completed successfully", "encrypt")

            return encrypted_base64

        except Exception as e:
            log_impl.log_error(f"Error during encryption: {e}", "encrypt", f"Error: {e}")
            raise RuntimeError("Error encrypting the secret")
