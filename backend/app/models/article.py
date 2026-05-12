"""
app/models/article.py
Pydantic schemas — shared between routes and responses.
"""
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


# ── Article (output) ───────────────────────────────────────────────────────────
class ArticleOut(BaseModel):
    pmid:     str
    title:    str
    authors:  List[str]
    abstract: Optional[str] = None
    journal:  Optional[str] = None
    year:     Optional[int] = None
    domain:   Optional[str] = None

    class Config:
        # Allow population from MongoDB dicts (with _id)
        populate_by_name = True


# ── Paginated wrapper ──────────────────────────────────────────────────────────
class PaginatedArticles(BaseModel):
    total:   int
    page:    int
    limit:   int
    pages:   int
    results: List[ArticleOut]


# ── Stats models ───────────────────────────────────────────────────────────────
class YearStat(BaseModel):
    year:  Optional[int] = Field(None, alias="_id")
    count: int

    class Config:
        populate_by_name = True


class DomainStat(BaseModel):
    domain:    Optional[str] = Field(None, alias="_id")
    count:     int
    avg_year:  Optional[float] = None

    class Config:
        populate_by_name = True


# ── Generic error ──────────────────────────────────────────────────────────────
class ErrorResponse(BaseModel):
    detail: str
