from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_dir: Path = Path("models/best_ncnn_model")
    img_size: int = 224
    confidence_threshold: float = 0.60   # below this -> "uncertain"
    max_upload_mb: int = 8
    app_name: str = "maize-disease-classifier"

settings = Settings()