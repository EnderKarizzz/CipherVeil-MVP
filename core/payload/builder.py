MAGIC = b"CVEIL001"
VERSION = 2 # Diperbarui ke versi 2[cite: 16]
HEADER_SIZE = 42 #[cite: 16]

def build_header(salt: bytes, nonce: bytes, encrypted_length: int, mode: int = 1) -> bytes:
    if len(salt) != 16 or len(nonce) != 12:
        raise ValueError("Metadata tidak valid")
    if not 16 <= encrypted_length <= 0xFFFFFFFF:
        raise ValueError("Panjang enkripsi tidak valid")
    if mode not in (1, 2, 3):
        raise ValueError("Mode tidak didukung")

    # Header v2: Magic(8) + Version(1) + Length(4) + Salt(16) + Nonce(12) + Mode(1) = 42 bytes[cite: 16, 17]
    return (
        MAGIC
        + VERSION.to_bytes(1, "big")
        + encrypted_length.to_bytes(4, "big")
        + salt
        + nonce
        + mode.to_bytes(1, "big")
    )

def build_payload(header: bytes, encrypted_data: bytes) -> bytes:
    if len(header) != HEADER_SIZE:
        raise ValueError("Header tidak valid")
    return header + encrypted_data