"""
app/core/utils.py
Shared helpers used across routes.
"""
from typing import Any
import math


def serialize_doc(doc: dict) -> dict:
    """Convert MongoDB document to JSON-safe dict (ObjectId → str)."""
    doc["_id"] = str(doc["_id"]) if "_id" in doc else None
    return doc


def build_pagination(total: int, page: int, limit: int) -> dict:
    """Return pagination metadata."""
    return {
        "total": total,
        "page":  page,
        "limit": limit,
        "pages": math.ceil(total / limit) if limit else 1,
    }
