import time
from functools import lru_cache
from ultralytics import YOLO
from app.config import settings

class ClassifierModel:
    """Thin wrapper around the exported NCNN model. Loaded once, reused per request."""

    def __init__(self, model_dir: str):
        self._model = YOLO(model_dir, task="classify")
        self.class_names: dict[int, str] = self._model.names

    def predict(self, image) -> tuple[list[tuple[str, float]], float]:
        start = time.perf_counter()
        results = self._model.predict(
            source=image,
            imgsz=settings.img_size,
            verbose=False,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        probs = results[0].probs
        top5_idx = probs.top5
        top5_conf = probs.top5conf.tolist()

        ranked = [(self.class_names[i], float(c)) for i, c in zip(top5_idx, top5_conf)]
        return ranked, elapsed_ms


@lru_cache(maxsize=1)
def get_model() -> ClassifierModel:
    return ClassifierModel(str(settings.model_dir))

