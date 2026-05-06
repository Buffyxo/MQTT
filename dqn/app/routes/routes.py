from fastapi import FastAPI
from fastapi.responses import JSONResponse
app = FastAPI()

@app.get("/")
@app.get("/health")
def health_check():
    """Status check"""
    return JSONResponse(status_code=200, content={"status": "healthy"})