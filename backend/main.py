"""
main.py
Entry point — run with:
    uvicorn main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes.articles import router as articles_router
from app.routes.stats    import router as stats_router
from database_manager    import DatabaseClient

# ── App instance ───────────────────────────────────────────────────────────────
app = FastAPI(
    title       = "🧬 Biomedical Corpus API",
    description = (
        "REST API for exploring the PubMed biomedical corpus stored in MongoDB.\n\n"
        "**Domains covered:** Cancer · COVID\n\n"
        "**Sources:** PubMed · PubMed Central (PMC) · Semantic Scholar\n\n"
        "---\n"
        "Built with **FastAPI** + **PyMongo** — Project 6 (Data Warehouse & Big Data)."
    ),
    version     = "1.0.0",
    contact     = {"name": "Backend Developer", "email": "dev@university.dz"},
    license_info= {"name": "Academic use only"},
    docs_url    = "/docs",
    redoc_url   = "/redoc",
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],   # Restrict to your frontend domain in production
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(articles_router)
app.include_router(stats_router)

# ── Global error handlers ──────────────────────────────────────────────────────
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code = exc.status_code,
        content     = {"detail": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code = 422,
        content     = {"detail": str(exc)},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code = 500,
        content     = {"detail": "Internal server error. Please try again later."},
    )

# ── Root & Health ──────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"], summary="API root")
def root():
    return {
        "api":     "Biomedical Corpus API",
        "version": "1.0.0",
        "docs":    "/docs",
        "status":  "running",
    }


@app.get("/health", tags=["Health"], summary="Database health check")
def health():
    db_ok = DatabaseClient().ping()
    return {
        "status":   "ok" if db_ok else "degraded",
        "database": "connected" if db_ok else "unreachable",
    }
