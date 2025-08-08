from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.cleaners import router as cleaners_router
from .routers.bookings import router as bookings_router
from .routers.applications import router as applications_router
from .routers.facebook import router as facebook_router


def create_app() -> FastAPI:
    app = FastAPI(title="CleanFee API", version="0.1.0")

    # CORS: allow Streamlit local and Streamlit Cloud by default; adjust as needed
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:8501",
            "http://127.0.0.1:8501",
        ],
        allow_origin_regex=r"https://.*\.streamlit\.app",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/healthz", tags=["system"]) 
    def healthz():
        return {"status": "ok"}

    app.include_router(cleaners_router, prefix="/api", tags=["cleaners"]) 
    app.include_router(bookings_router, prefix="/api", tags=["bookings"]) 
    app.include_router(applications_router, prefix="/api", tags=["applications"]) 
    app.include_router(facebook_router, prefix="/api", tags=["facebook"]) 

    return app


app = create_app()


