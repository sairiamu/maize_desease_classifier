from pydantic import BaseModel, Field

class Prediction(BaseModel):
    class_name: str
    display_name: str
    confidence: float = Field(..., ge=0, le=1)
    category: str

class PredictResponse(BaseModel):
    success: bool
    is_confident: bool
    prediction: Prediction
    top_k: list[Prediction]
    causal_agent: str
    severity_note: str
    recommendations: list[str]
    inference_ms: float

class ErrorResponse(BaseModel):
    success: bool = False
    error: str