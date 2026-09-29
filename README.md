# Maize Disease Classifier

FastAPI service for classifying maize leaf images with an NCNN model.

## Model files

Place the exported NCNN files in `models/best_ncnn_model/` using these names:

- `model.param`
- `model.bin`

The default input and output blob names are `data` and `output`. Set `NCNN_INPUT_BLOB` and `NCNN_OUTPUT_BLOB` if your export uses different names. `CLASS_NAMES` is a comma-separated list ordered exactly like the model output; its default is `Blight,Common_Rust,Gray_Leaf_Spot,Healthy`.

Optional settings include `MODEL_DIR`, `NCNN_PARAM_PATH`, `NCNN_BIN_PATH`, `IMAGE_SIZE`, `CONFIDENCE_THRESHOLD`, and `MAX_IMAGE_BYTES`.

## Run locally

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API docs are available at `http://localhost:8000/docs`. `GET /health` reports whether the model is ready; `POST /predict` accepts an image in a multipart form field named `file`.

## Test

```powershell
pytest
```

## Run with Docker

```powershell
docker build -t maize-disease-classifier .
docker run --rm -p 8000:8000 maize-disease-classifier
```

The API requires valid NCNN model artifacts at runtime. The recommendation text is general guidance, not a substitute for diagnosis by a local agronomist.
