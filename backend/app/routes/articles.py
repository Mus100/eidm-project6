"""
app/routes/articles.py
Routes:
  GET /articles          — list with filters + pagination
  GET /articles/{pmid}   — single article by PMID
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from database_manager import DatabaseClient
from app.models.article import ArticleOut, PaginatedArticles, ErrorResponse
from app.core.utils import serialize_doc, build_pagination

router = APIRouter(prefix="/articles", tags=["Articles"])

# One shared collection handle
_col = DatabaseClient().get_db_connection()


# ── GET /articles ──────────────────────────────────────────────────────────────
@router.get(
    "",
    response_model=PaginatedArticles,
    summary="List articles",
    description=(
        "Retrieve articles with optional filters: **domain**, **year range**, "
        "and **full-text search** on title + abstract. Results are paginated."
    ),
    responses={404: {"model": ErrorResponse, "description": "No articles found"}},
)
def list_articles(
    domain:    Optional[str] = Query(None,  description="Filter by domain: Cancer or COVID"),
    search:    Optional[str] = Query(None,  description="Full-text search on title and abstract"),
    year_from: Optional[int] = Query(None,  description="Filter articles published from this year"),
    year_to:   Optional[int] = Query(None,  description="Filter articles published up to this year"),
    page:      int           = Query(1,     ge=1,  description="Page number (starts at 1)"),
    limit:     int           = Query(10,    ge=1, le=100, description="Results per page (max 100)"),
):
    query: dict = {}

    # Domain filter
    if domain:
        query["domain"] = domain

    # Year range filter
    year_filter: dict = {}
    if year_from is not None:
        year_filter["$gte"] = year_from
    if year_to is not None:
        year_filter["$lte"] = year_to
    if year_filter:
        query["year"] = year_filter

    # Full-text search (uses idx_text_search on title + abstract)
    if search:
        query["$text"] = {"$search": search}

    total = _col.count_documents(query)

    if total == 0:
        raise HTTPException(status_code=404, detail="No articles found matching the given criteria.")

    skip   = (page - 1) * limit
    cursor = _col.find(query, {"_id": 0}).sort("year", -1).skip(skip).limit(limit)
    docs   = [ArticleOut(**serialize_doc(d)) for d in cursor]

    return PaginatedArticles(
        **build_pagination(total, page, limit),
        results=docs,
    )


# ── GET /articles/{pmid} ───────────────────────────────────────────────────────
@router.get(
    "/{pmid}",
    response_model=ArticleOut,
    summary="Get article by PMID",
    description="Retrieve a single article using its unique **PubMed ID (PMID)**.",
    responses={404: {"model": ErrorResponse, "description": "Article not found"}},
)
def get_article(pmid: str):
    doc = _col.find_one({"pmid": pmid}, {"_id": 0})

    if not doc:
        raise HTTPException(status_code=404, detail=f"Article with PMID '{pmid}' not found.")

    return ArticleOut(**serialize_doc(doc))
