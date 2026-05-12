"""
app/routes/stats.py
Routes:
  GET /stats/year    — article count grouped by year
  GET /stats/domain  — article count + avg year grouped by domain
"""
from fastapi import APIRouter, HTTPException
from typing import List

from database_manager import DatabaseClient
from app.models.article import YearStat, DomainStat, ErrorResponse

router = APIRouter(prefix="/stats", tags=["Statistics"])

_col = DatabaseClient().get_db_connection()


# ── GET /stats/year ────────────────────────────────────────────────────────────
@router.get(
    "/year",
    response_model=List[YearStat],
    summary="Articles per year",
    description="Returns the **total number of articles** grouped by publication year, sorted ascending.",
    responses={404: {"model": ErrorResponse, "description": "No data available"}},
)
def stats_by_year():
    pipeline = [
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort":  {"_id": 1}},
    ]
    results = list(_col.aggregate(pipeline))

    if not results:
        raise HTTPException(status_code=404, detail="No statistics available — collection may be empty.")

    return [YearStat(**r) for r in results]


# ── GET /stats/domain ──────────────────────────────────────────────────────────
@router.get(
    "/domain",
    response_model=List[DomainStat],
    summary="Articles per domain",
    description=(
        "Returns the **total number of articles** and the **average publication year** "
        "for each medical domain (Cancer, COVID, …)."
    ),
    responses={404: {"model": ErrorResponse, "description": "No data available"}},
)
def stats_by_domain():
    pipeline = [
        {
            "$group": {
                "_id":      "$domain",
                "count":    {"$sum": 1},
                "avg_year": {"$avg": "$year"},
            }
        },
        {"$sort": {"count": -1}},
    ]
    results = list(_col.aggregate(pipeline))

    if not results:
        raise HTTPException(status_code=404, detail="No statistics available — collection may be empty.")

    return [DomainStat(**r) for r in results]
