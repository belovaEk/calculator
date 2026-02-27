from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.base import api_router
import uvicorn

LOCAL_ORIGIN_REGEX = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


def start_application():

    app = FastAPI(title="Calculator", version="beta")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=LOCAL_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        max_age=86400,
    )

    app.include_router(api_router)
    return app


app = start_application()


if __name__ == "__main__":
    # Используем строку "main:app", чтобы uvicorn
    # мог корректно перезапускать процесс с reload.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
