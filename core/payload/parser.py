MAGIC = b"CVEIL001"
VERSION = 2

def parse_header(header: bytes) -> dict:
    if len(header) != 42:
        raise ValueError("Ukuran header tidak sesuai.")
    if header[0:8] != MAGIC:
        raise ValueError("Magic signature tidak ditemukan.")
    if header[8] != VERSION:
        raise ValueError("Versi payload tidak didukung.")
    
    return {
        "encrypted_length": int.from_bytes(header[9:13], "big"),
        "salt": header[13:29],
        "nonce": header[29:41],
        "mode": header[41],
        "raw_header": header
    }