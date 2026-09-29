from typing import TypedDict

class ClassInfo(TypedDict):
    display_name: str
    category: str          # "disease" | "deficiency" | "healthy"
    causal_agent: str
    severity_note: str
    recommendations: list[str]

# NOTE: only Blight and Common_Rust exist in the current model (nc=2).
# Add entries here as you train on more classes (Healthy, N_deficiency, etc.)
CLASS_METADATA: dict[str, ClassInfo] = {
    "Blight": {
        "display_name": "Northern Corn Leaf Blight",
        "category": "disease",
        "causal_agent": "Exserohilum turcicum (fungal)",
        "severity_note": "Can cause significant yield loss if it reaches the ear leaf before tasseling.",
        "recommendations": [
            "Apply a foliar fungicide (e.g. strobilurin or triazole-based) if lesions are spreading.",
            "Rotate away from maize/sorghum for at least one season to break the disease cycle.",
            "Remove and destroy infected crop residue after harvest instead of tilling it under.",
            "Consider blight-resistant hybrids for the next planting.",
        ],
    },
    "Common_Rust": {
        "display_name": "Common Rust",
        "category": "disease",
        "causal_agent": "Puccinia sorghi (fungal)",
        "severity_note": "Usually minor unless infection is heavy and early in the season.",
        "recommendations": [
            "Monitor severity — light rust rarely needs treatment on mature plants.",
            "Apply fungicide only if pustules cover a large leaf area before tasseling.",
            "Favor rust-resistant hybrids in future planting.",
            "Avoid dense planting/over-fertilizing with nitrogen, which increases susceptibility.",
        ],
    },
}

UNKNOWN_CLASS_INFO: ClassInfo = {
    "display_name": "Unclassified / Low Confidence",
    "category": "unknown",
    "causal_agent": "n/a",
    "severity_note": "Model confidence too low to trust this prediction.",
    "recommendations": [
        "Retake the photo in better lighting, closer to the leaf, avoiding blur.",
        "Consult a local agronomist if symptoms persist.",
    ],
}

def get_class_info(class_name: str, confident: bool) -> ClassInfo:
    if not confident:
        return UNKNOWN_CLASS_INFO
    return CLASS_METADATA.get(class_name, UNKNOWN_CLASS_INFO)