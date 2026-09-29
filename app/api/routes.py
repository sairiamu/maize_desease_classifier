from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.domain.recommendations import get_class_info
from app.inference.model import get_model
from app.inference.preprocess import load_image
from app.schemas import ErrorResponse, PredictResponse, Prediction

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post(
    "/predict",
    response_model=PredictResponse,
    responses={400: {"model": ErrorResponse}},
)
async def predict(file: UploadFile = File(...)):
    if file.size and file.size > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"File exceeds {settings.max_upload_mb}MB limit.")

    raw = await file.read()
    try:
        image = load_image(raw)
    except ValueError as e:
        raise HTTPException(400, str(e))

    model = get_model()
    ranked, elapsed_ms = model.predict(image)

    top_class, top_conf = ranked[0]
    is_confident = top_conf >= settings.confidence_threshold
    info = get_class_info(top_class, is_confident)

    top_k = [
        Prediction(
            class_name=name,
            display_name=get_class_info(name, True)["display_name"],
            confidence=round(conf, 4),
            category=get_class_info(name, True)["category"],
        )
        for name, conf in ranked
    ]

    return PredictResponse(
        success=True,
        is_confident=is_confident,
        prediction=Prediction(
            class_name=top_class,
            display_name=info["display_name"],
            confidence=round(top_conf, 4),
            category=info["category"],
        ),
        top_k=top_k,
        causal_agent=info["causal_agent"],
        severity_note=info["severity_note"],
        recommendations=info["recommendations"],
        inference_ms=round(elapsed_ms, 2),
    )
