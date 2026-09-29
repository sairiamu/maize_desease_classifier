# from fastapi import FastAPI
# from app.api.routes import router
# from app.config import settings
# import uvicorn

# app = FastAPI(title=settings.app_name)
# app.include_router(router)

from fastapi import FastAPI 
from app.api.routes import router 
from app.config import settings 
import uvicorn 

app = FastAPI(title=settings.app_name) 
app.include_router(router) 

if __name__ == "__main__": 
    # Runs the app internally on http://127.0.0.1:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
