def validate_pdf(data: bytes):
    if not data.startswith(b"%PDF-"):
        raise ValueError("File yang diunggah bukan PDF yang valid.")

def validate_capacity(width: int, height: int, payload_size: int):
    available_capacity = (width * height * 3) // 8
    if payload_size > available_capacity:
        raise ValueError(f"Kapasitas gambar tidak cukup. Tersedia: {available_capacity} bytes, Butuh: {payload_size} bytes.")