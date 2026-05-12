# Schema MongoDB — `pubmed_db.articles`

Documentation pour le **Backend Developer** (Flask / FastAPI).

---

## Structure d'un document

```json
{
  "_id":      "ObjectId autogénéré",
  "pmid":     "39123456",
  "title":    "Efficacy of mRNA vaccines against COVID-19 variants",
  "authors":  ["Dupont, J", "Martin, A", "Lee, C"],
  "abstract": "Background: ... Methods: ... Results: ...",
  "journal":  "The Lancet",
  "year":     2023,
  "domain":   "COVID"
}
```

### Champs — types & notes

| Champ      | Type MongoDB | Note                                          |
|------------|--------------|-----------------------------------------------|
| `_id`      | ObjectId     | Clé primaire auto                             |
| `pmid`     | String       | **Index unique** — clé métier (NCBI PubMed)   |
| `title`    | String       | Indexé en Text Search                         |
| `authors`  | Array[String]| Format `"NomDeFamille, Initiales"`            |
| `abstract` | String       | Indexé en Text Search (tronqué à 300 chars)   |
| `journal`  | String       | Nom complet du journal                        |
| `year`     | Integer      | `null` si donnée absente dans la source       |
| `domain`   | String       | `"Cancer"` ou `"COVID"` (déduit du fichier)   |

---

## Index disponibles

| Nom index           | Champ(s)              | Type        | Usage                          |
|---------------------|-----------------------|-------------|--------------------------------|
| `idx_pmid_unique`   | `pmid`                | Unique       | Évite les doublons             |
| `idx_year`          | `year`                | Ascending    | Tri / filtre par année         |
| `idx_domain`        | `domain`              | Ascending    | Filtre par domaine médical     |
| `idx_text_search`   | `title` + `abstract`  | Text         | Recherche plein-texte          |

---

## Exemples de requêtes PyMongo pour tes routes Flask/FastAPI

### `GET /articles` — Tous les articles d'un domaine

```python
from database_manager import DatabaseClient

col = DatabaseClient().get_db_connection()

# Tous les articles COVID, triés par année décroissante
results = list(col.find({"domain": "COVID"}).sort("year", -1))
```

### `GET /articles?search=vaccine` — Recherche plein-texte

```python
results = list(col.find({"$text": {"$search": "vaccine"}}))
```

### `GET /articles?year_from=2020&year_to=2024` — Filtre par période

```python
results = list(col.find({"year": {"$gte": 2020, "$lte": 2024}}))
```

### `GET /articles/{pmid}` — Article unique

```python
article = col.find_one({"pmid": "39123456"})
```

### `GET /stats` — Statistiques globales

```python
pipeline = [
    {"$group": {"_id": "$domain", "count": {"$sum": 1}, "avg_year": {"$avg": "$year"}}}
]
stats = list(col.aggregate(pipeline))
```

---

## Import rapide dans Flask ou FastAPI

```python
# Dans ton fichier app.py ou routes.py
from database_manager import DatabaseClient

_client = DatabaseClient()          # une seule instance (singleton)
col = _client.get_db_connection()   # objet Collection réutilisable
```

> **Note :** Instancie `DatabaseClient` **une seule fois** au démarrage de l'app,
> puis passe `col` à tes routes. Cela évite d'ouvrir une nouvelle connexion à chaque requête.
