import uvicorn
from config import settings
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def health_check():
    response = {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
    return response

if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT, log_level="info")
