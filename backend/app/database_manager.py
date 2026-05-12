"""
database_manager.py
Singleton MongoDB connection — import this everywhere.
"""
import os
from pymongo import MongoClient
from pymongo.collection import Collection
from dotenv import load_dotenv

load_dotenv()


class DatabaseClient:
    _instance: "DatabaseClient | None" = None
    _client: MongoClient | None = None

    # ── Singleton ──────────────────────────────────────────────────────────
    def __new__(cls) -> "DatabaseClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connect()
        return cls._instance

    # ── Private helpers ────────────────────────────────────────────────────
    def _connect(self) -> None:
        uri        = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name    = os.getenv("MONGO_DB_NAME", "pubmed_db")
        collection = os.getenv("MONGO_COLLECTION", "articles")

        self._client     = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self._db         = self._client[db_name]
        self._collection = self._db[collection]

    # ── Public API ─────────────────────────────────────────────────────────
    def get_db_connection(self) -> Collection:
        """Return the articles Collection object."""
        return self._collection

    def ping(self) -> bool:
        """Quick health-check — returns True if Mongo is reachable."""
        try:
            self._client.admin.command("ping")
            return True
        except Exception:
            return False
