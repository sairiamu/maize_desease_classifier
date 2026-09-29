import io
from PIL import Image, UnidentifiedImageError

ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}

def load_image(raw_bytes: bytes) -> Image.Image:
    try:
        img = Image.open(io.BytesIO(raw_bytes))
        img.verify()
        img = Image.open(io.BytesIO(raw_bytes))  # re-open after verify()
    except UnidentifiedImageError:
        raise ValueError("File is not a valid image.")

    if img.format not in ALLOWED_FORMATS:
        raise ValueError(f"Unsupported format: {img.format}")

    return img.convert("RGB")

    