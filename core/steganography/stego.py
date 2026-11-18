import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

HEADER_BITS = 42 * 8  # 336 bits[cite: 17, 18]

def sort_keys(seed: bytes, count: int) -> np.ndarray:
    enc = Cipher(algorithms.AES(seed), modes.CTR(bytes(16))).encryptor()
    stream = enc.update(bytes((count * 8) + 16))
    return np.frombuffer(stream[:count*8], dtype='<u8') #[cite: 18]

def edge_magnitude(rgb: np.ndarray) -> np.ndarray:
    base = rgb.astype(np.int32) & 0xFE
    gray = (base[..., 0] * 299 + base[..., 1] * 587 + base[..., 2] * 114) // 1000
    g = np.pad(gray, 1, mode='edge')
    gx = (g[:-2, 2:] + 2 * g[1:-1, 2:] + g[2:, 2:]) - (g[:-2, :-2] + 2 * g[1:-1, :-2] + g[2:, :-2])
    gy = (g[2:, :-2] + 2 * g[2:, 1:-1] + g[2:, 2:]) - (g[:-2, :-2] + 2 * g[:-2, 1:-1] + g[:-2, 2:])
    return np.abs(gx) + np.abs(gy) #[cite: 19]

def get_body_positions(rgb: np.ndarray, mode: int, seed: bytes, body_bits_count: int) -> np.ndarray:
    total_bits = rgb.size
    
    if mode == 1:
        # Mode 1: Sekuensial[cite: 18]
        return np.arange(HEADER_BITS, HEADER_BITS + body_bits_count)
    
    elif mode == 2:
        # Mode 2: Acak[cite: 18]
        universe = total_bits - HEADER_BITS
        order = np.argsort(sort_keys(seed, universe), kind='stable')
        return HEADER_BITS + order[:body_bits_count]
    
    elif mode == 3:
        # Mode 3: Adaptif Tepi[cite: 19]
        mag = edge_magnitude(rgb).ravel()
        header_pixels = HEADER_BITS // 3
        k_pixels = int(np.ceil(body_bits_count / 3.0))
        cand = np.arange(header_pixels, mag.size)
        order = np.lexsort((cand, -mag[cand]))
        chosen_pixels = cand[order[:k_pixels]]
        sorted_pixels = chosen_pixels[np.argsort(sort_keys(seed, k_pixels), kind='stable')]
        
        # Ekstrak posisi bit dari piksel terpilih
        bit_positions = (sorted_pixels[:, None] * 3 + np.arange(3)).ravel()
        return bit_positions[:body_bits_count]
    else:
        raise ValueError("Mode penempatan bit tidak valid.")

def encode_image(rgb: np.ndarray, payload: bytes, mode: int, seed: bytes) -> np.ndarray:
    bits = np.unpackbits(np.frombuffer(payload, dtype=np.uint8))
    flat_img = rgb.ravel()
    
    # 1. Tulis Header (Selalu Sekuensial)[cite: 18, 20]
    flat_img[:HEADER_BITS] = (flat_img[:HEADER_BITS] & 0xFE) | bits[:HEADER_BITS]
    
    # 2. Tulis Isi Paket (Berdasarkan Mode)[cite: 20]
    body_bits = bits[HEADER_BITS:]
    positions = get_body_positions(rgb, mode, seed, len(body_bits))
    flat_img[positions] = (flat_img[positions] & 0xFE) | body_bits
    
    return flat_img.reshape(rgb.shape)

def decode_header(rgb: np.ndarray) -> bytes:
    flat_img = rgb.ravel()
    header_bits = flat_img[:HEADER_BITS] & 1
    return np.packbits(header_bits).tobytes()

def decode_body(rgb: np.ndarray, mode: int, seed: bytes, encrypted_length: int) -> bytes:
    flat_img = rgb.ravel()
    body_bits_count = encrypted_length * 8
    positions = get_body_positions(rgb, mode, seed, body_bits_count)
    body_bits = flat_img[positions] & 1
    return np.packbits(body_bits).tobytes()