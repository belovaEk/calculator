from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.base import api_router
import uvicorn

LOCAL_ORIGIN_REGEX = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"

# origins = [
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
#     "http://localhost:8080", 
#     "http://127.0.0.1:8080",  
#     "http://localhost:8081", 
#     "http://127.0.0.1:8081",
#     "http://localhost:8082", 
#     "http://127.0.0.1:8082",
#     "http://192.168.0.170:8081",
# ]

def start_application():

    app = FastAPI(title="Calculator", version="beta")

    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

    app.include_router(api_router)
    return app


app = start_application()


if __name__ == "__main__":
    # Используем строку "main:app", чтобы uvicorn
    # мог корректно перезапускать процесс с reload.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
