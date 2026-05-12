"""
database_manager.py
====================
Classe DatabaseClient — Interface MongoDB Atlas réutilisable.
Ton coéquipier Backend peut importer directement :
    from database_manager import DatabaseClient
"""

import os
import pandas as pd
from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import DuplicateKeyError, BulkWriteError
from dotenv import load_dotenv
import dns.resolver
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']

load_dotenv()  # Charge les variables depuis .env


class DatabaseClient:
    """
    Client MongoDB Atlas centralisé.
    Fournit insert_data() et get_db_connection() pour le Backend.
    """

    def __init__(self):
        uri = os.getenv("MONGODB_URI")
        db_name = os.getenv("MONGODB_DB", "biomedical_corpus")
        collection_name = os.getenv("MONGODB_COLLECTION", "articles")

        if not uri:
            raise EnvironmentError(
                "❌ MONGODB_URI introuvable. Vérifie ton fichier .env"
            )

        self._client = MongoClient(uri, tlsAllowInvalidCertificates=True)
        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

        self._ensure_indexes()
        print(f"✅ Connecté à MongoDB Atlas — base: '{db_name}', collection: '{collection_name}'")

    # ------------------------------------------------------------------
    # MÉTHODE 1 : connexion réutilisable pour le Backend
    # ------------------------------------------------------------------
    def get_db_connection(self):
        """
        Retourne l'objet Collection MongoDB.
        Usage Backend :
            from database_manager import DatabaseClient
            db = DatabaseClient().get_db_connection()
            articles = list(db.find({"domain": "Cancer"}))
        """
        return self._collection

    # ------------------------------------------------------------------
    # MÉTHODE 2 : chargement et insertion des CSV
    # ------------------------------------------------------------------
    def insert_data(self, file_path: str) -> dict:
        """
        Charge un CSV PubMed et insère les documents dans MongoDB.
        Évite les doublons grâce à l'index unique sur PMID.

        Args:
            file_path: Chemin vers le fichier CSV (ex: "MES_ARTICLES_CANCER.csv")

        Returns:
            dict avec les clés 'inserted', 'skipped', 'errors'
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ Fichier introuvable : {file_path}")

        # Détermination du domaine à partir du nom de fichier
        domain = self._infer_domain(file_path)
        print(f"\n📂 Chargement : {file_path}  →  domaine détecté : '{domain}'")

        df = pd.read_csv(file_path, encoding="utf-8-sig")
        print(f"   {len(df)} lignes lues")

        documents = [self._transform_row(row, domain) for _, row in df.iterrows()]

        inserted, skipped, errors = 0, 0, 0
        for doc in documents:
            try:
                self._collection.insert_one(doc)
                inserted += 1
            except DuplicateKeyError:
                skipped += 1
            except Exception as e:
                print(f"   ⚠️  Erreur PMID {doc.get('pmid')}: {e}")
                errors += 1

        print(f"   ✅ Insérés: {inserted}  |  ⏭  Doublons ignorés: {skipped}  |  ❌ Erreurs: {errors}")
        return {"inserted": inserted, "skipped": skipped, "errors": errors}

    # ------------------------------------------------------------------
    # MÉTHODE UTILITAIRE : statistiques rapides
    # ------------------------------------------------------------------
    def stats(self) -> dict:
        """Retourne un résumé de la base pour le Backend (/stats route)."""
        pipeline = [
            {"$group": {"_id": "$domain", "count": {"$sum": 1}}}
        ]
        by_domain = {r["_id"]: r["count"] for r in self._collection.aggregate(pipeline)}
        return {
            "total_articles": self._collection.count_documents({}),
            "by_domain": by_domain
        }

    # ------------------------------------------------------------------
    # MÉTHODES PRIVÉES
    # ------------------------------------------------------------------
    def _ensure_indexes(self):
        """Crée les index au premier lancement (opération idempotente)."""
        # Index unique sur PMID — évite les doublons
        self._collection.create_index("pmid", unique=True, name="idx_pmid_unique")
        # Index simple sur year et domain — filtres rapides
        self._collection.create_index([("year", ASCENDING)], name="idx_year")
        self._collection.create_index([("domain", ASCENDING)], name="idx_domain")
        # Text index pour recherche plein-texte
        self._collection.create_index(
            [("title", TEXT), ("abstract", TEXT)],
            name="idx_text_search",
            default_language="english"
        )
        print("   📌 Index vérifiés / créés")

    @staticmethod
    def _transform_row(row: pd.Series, domain: str) -> dict:
        """
        Transforme une ligne CSV en document MongoDB structuré.
        - Auteurs : str → list
        - Année   : str → int (ou None si invalide)
        - Ajout du champ domain
        """
        # Auteurs : "Dupont, J; Martin, A" → ["Dupont, J", "Martin, A"]
        authors_raw = str(row.get("Auteurs", "") or "")
        authors = [a.strip() for a in authors_raw.split(";") if a.strip()] or []

        # Année : conversion en entier
        try:
            year = int(row.get("Année", 0))
        except (ValueError, TypeError):
            year = None

        return {
            "pmid":     str(row.get("PMID", "")).strip(),
            "title":    str(row.get("Titre", "")).strip(),
            "authors":  authors,
            "abstract": str(row.get("Résumé", "")).strip(),
            "journal":  str(row.get("Journal", "")).strip(),
            "year":     year,
            "domain":   domain,
        }

    @staticmethod
    def _infer_domain(file_path: str) -> str:
        """Déduit le domaine depuis le nom de fichier."""
        name = os.path.basename(file_path).upper()
        if "COVID" in name:
            return "COVID"
        if "CANCER" in name:
            return "Cancer"
        # Fallback : nom de fichier sans extension
        return os.path.splitext(os.path.basename(file_path))[0]


# ------------------------------------------------------------------
# POINT D'ENTRÉE : script autonome
# ------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    client = DatabaseClient()

    # Fichiers à insérer (passer en argument ou liste par défaut)
    files = sys.argv[1:] if len(sys.argv) > 1 else [
        "MES_ARTICLES_CANCER.csv",
        "MES_ARTICLES_COVID.csv",
    ]

    for f in files:
        if os.path.exists(f):
            client.insert_data(f)
        else:
            print(f"⚠️  Fichier ignoré (introuvable) : {f}")

    print("\n📊 Statistiques de la base :")
    print(client.stats())
