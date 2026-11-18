from PIL import Image
import numpy as np
from io import BytesIO

def load_image(image_bytes: bytes) -> np.ndarray:
    img = Image.open(BytesIO(image_bytes))
    img.load()
    return np.array(img.convert("RGB"))

def save_as_png(image_array: np.ndarray) -> bytes:
    img = Image.fromarray(image_array, 'RGB')
    output = BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()