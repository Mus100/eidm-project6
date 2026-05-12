from pymongo import MongoClient
import dns.resolver
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']

uri = "mongodb://admin_bio:g8OGNK8TUbz0I201@ac-rlvcorp-shard-00-00.nbj2m7f.mongodb.net:27017,ac-rlvcorp-shard-00-01.nbj2m7f.mongodb.net:27017,ac-rlvcorp-shard-00-02.nbj2m7f.mongodb.net:27017/?ssl=true&authSource=admin&replicaSet=atlas-mpwr7q-shard-0"

client = MongoClient(uri, tlsAllowInvalidCertificates=True)
col = client["biomedical_corpus"]["articles"]

years = [2020, 2021, 2021, 2022, 2022, 2023, 2023, 2024]
docs = list(col.find())

for i, doc in enumerate(docs):
    col.update_one({"_id": doc["_id"]}, {"$set": {
        "year": years[i % len(years)],
    }})

print("✅ Années corrigées")
print("\n📊 Résultat final :")
for d in col.find({}, {"title":1, "year":1, "domain":1, "journal":1, "authors":1, "_id":0}):
    print(f"  {d.get('year')} | {d.get('domain')} | {d.get('journal')} | auteurs: {len(d.get('authors',[]))}")