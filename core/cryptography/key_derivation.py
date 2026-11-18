import os
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

SALT_LENGTH = 16
KEY_LENGTH = 32
ARGON2_TIME_COST = 3
ARGON2_MEMORY_COST = 65536
ARGON2_PARALLELISM = 4

def generate_salt() -> bytes:
    return os.urandom(SALT_LENGTH)

def derive_key(password: str, salt: bytes) -> bytes:
    if not password:
        raise ValueError("Password tidak boleh kosong")
    if len(salt) != SALT_LENGTH:
        raise ValueError("Salt tidak valid")

    return hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=ARGON2_TIME_COST,
        memory_cost=ARGON2_MEMORY_COST,
        parallelism=ARGON2_PARALLELISM,
        hash_len=KEY_LENGTH,
        type=Type.ID
    )

def derive_position_seed(key: bytes) -> bytes:
    # Fungsi turunan spesifikasi Paket 2 untuk seed posisi bit
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'cipherveil-pos-v2',
    ).derive(key) #[cite: 17]