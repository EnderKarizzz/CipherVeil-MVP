from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE_LENGTH = 12

def encrypt(plaintext: bytes, key: bytes, nonce: bytes, aad: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("Kunci AES-256 tidak valid")
    if len(nonce) != NONCE_LENGTH:
        raise ValueError("Nonce tidak valid")
    
    return AESGCM(key).encrypt(nonce, plaintext, aad)

def decrypt(ciphertext: bytes, key: bytes, nonce: bytes, aad: bytes) -> bytes:
    return AESGCM(key).decrypt(nonce, ciphertext, aad)