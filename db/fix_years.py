from pymongo import MongoClient
import random

uri = "mongodb://admin_bio:g8OGNK8TUbz0I201@ac-rlvcorp-shard-00-00.nbj2m7f.mongodb.net:27017,ac-rlvcorp-shard-00-01.nbj2m7f.mongodb.net:27017,ac-rlvcorp-shard-00-02.nbj2m7f.mongodb.net:27017/?ssl=true&authSource=admin&replicaSet=atlas-mpwr7q-shard-0"

client = MongoClient(uri, tlsAllowInvalidCertificates=True)
col = client["biomedical_corpus"]["articles"]

years = [2020, 2021, 2021, 2022, 2022, 2023, 2023, 2024]
docs  = list(col.find({}, {"_id": 1}))

for i, doc in enumerate(docs):
    col.update_one({"_id": doc["_id"]}, {"$set": {"year": years[i % len(years)]}})
    print(f"✅ Article {i+1} → année {years[i % len(years)]}")

print("✅ Années mises à jour !")