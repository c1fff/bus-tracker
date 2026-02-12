import uvicorn
from fastapi import FastAPI
from .tracking.views import router as tracking_router

app = FastAPI(title="Bus-GPS Track")

app.include_router(tracking_router)

@app.get("/")
def read_root():
    return {"Hello": "Dias"}

