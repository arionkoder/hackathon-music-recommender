from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import base


def create_app():
    app = FastAPI(
        openapi_url="/swagger.json",
        docs_url="/docs",
        redoc_url=None,
        root_path="",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "https://localhost:3000",
            "http://localhost:5000",
            "http://localhost",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(base.router)

    return app


app = create_app()
