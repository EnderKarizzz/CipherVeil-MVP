import os
from core.file.validator import validate_pdf, validate_capacity
from core.image.processor import load_image, save_as_png
from core.cryptography.key_derivation import generate_salt, derive_key, derive_position_seed
from core.cryptography.aes import encrypt, decrypt
from core.payload.builder import build_header, build_payload
from core.payload.parser import parse_header
from core.steganography.stego import encode_image, decode_header, decode_body

def embed_pdf(pdf_bytes: bytes, image_bytes: bytes, password: str, mode: int = 1) -> bytes:
    validate_pdf(pdf_bytes)
    
    img_array = load_image(image_bytes)
    h, w, _ = img_array.shape
    
    salt = generate_salt()
    nonce = os.urandom(12)
    encrypted_length = len(pdf_bytes) + 16
    payload_size = 42 + encrypted_length
    
    validate_capacity(w, h, payload_size)
    
    header = build_header(salt, nonce, encrypted_length, mode)
    key = derive_key(password, salt)
    ciphertext = encrypt(pdf_bytes, key, nonce, aad=header)
    
    payload = build_payload(header, ciphertext)
    position_seed = derive_position_seed(key)
    
    stego_array = encode_image(img_array, payload, mode, position_seed)
    return save_as_png(stego_array)

def extract_pdf(image_bytes: bytes, password: str) -> bytes:
    img_array = load_image(image_bytes)
    
    # 1. Baca Header v2[cite: 15, 20]
    raw_header = decode_header(img_array)
    header_dict = parse_header(raw_header)
    mode = header_dict["mode"]
    
    # 2. Turunkan Kunci & Seed Posisi[cite: 15, 20]
    key = derive_key(password, header_dict["salt"])
    position_seed = derive_position_seed(key)
    
    # 3. Ekstrak Isi Paket[cite: 15, 20]
    ciphertext = decode_body(img_array, mode, position_seed, header_dict["encrypted_length"])
    
    # 4. Dekripsi AES-256-GCM[cite: 15, 20]
    pdf_bytes = decrypt(ciphertext, key, header_dict["nonce"], aad=raw_header)
    validate_pdf(pdf_bytes)
    
    return pdf_bytes