# 🧬 Biomedical Corpus API

FastAPI backend for **Project 6 — Cloud Deployment** (Data Warehouse & Big Data).

Connects to a MongoDB collection (`pubmed_db.articles`) and exposes a REST API
for exploring a biomedical corpus (Cancer & COVID articles from PubMed / PMC / Semantic Scholar).

---

## Project Structure

```
biomedical_api/
├── main.py                   # App entry point, CORS, error handlers
├── database_manager.py       # MongoDB singleton connection
├── requirements.txt
├── .env.example              # ← copy to .env and fill in your values
└── app/
    ├── models/
    │   └── article.py        # Pydantic schemas (ArticleOut, Stats, …)
    ├── routes/
    │   ├── articles.py       # GET /articles  GET /articles/{pmid}
    │   └── stats.py          # GET /stats/year  GET /stats/domain
    └── core/
        └── utils.py          # Shared helpers (serialization, pagination)
```

---

## Setup

### 1. Clone & install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Local MongoDB
MONGO_URI=mongodb://localhost:27017

# MongoDB Atlas (cloud)
# MONGO_URI=mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/

MONGO_DB_NAME=pubmed_db
MONGO_COLLECTION=articles
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

API is available at `http://localhost:8000`

---

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | API info |
| GET | `/health` | MongoDB connection health check |
| GET | `/articles` | List articles (filters + pagination) |
| GET | `/articles/{pmid}` | Get a single article by PMID |
| GET | `/stats/year` | Article count per year |
| GET | `/stats/domain` | Article count + avg year per domain |

### `/articles` — Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `domain` | string | Filter by `Cancer` or `COVID` |
| `search` | string | Full-text search on title + abstract |
| `year_from` | int | Published from this year |
| `year_to` | int | Published up to this year |
| `page` | int | Page number (default: 1) |
| `limit` | int | Results per page (default: 10, max: 100) |

### Example Requests

```bash
# All COVID articles, page 2
GET /articles?domain=COVID&page=2&limit=20

# Full-text search for "vaccine"
GET /articles?search=vaccine

# Cancer articles between 2020 and 2023
GET /articles?domain=Cancer&year_from=2020&year_to=2023

# Single article
GET /articles/39123456

# Stats
GET /stats/year
GET /stats/domain
```

---

## Interactive Docs

- **Swagger UI** → `http://localhost:8000/docs`
- **ReDoc**       → `http://localhost:8000/redoc`

---

## Error Format

All errors return a consistent JSON body:

```json
{ "detail": "Human-readable error message here." }
```

| Status | Meaning |
|--------|---------|
| 404 | No results / article not found |
| 422 | Invalid query parameters |
| 500 | Server / database error |
