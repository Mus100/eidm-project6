from pymongo import MongoClient

uri = "mongodb://admin_bio:g8OGNK8TUbz0I201@ac-rlvcorp-shard-00-00.nbj2m7f.mongodb.net:27017,ac-rlvcorp-shard-00-01.nbj2m7f.mongodb.net:27017,ac-rlvcorp-shard-00-02.nbj2m7f.mongodb.net:27017/?ssl=true&authSource=admin"

try:
    client = MongoClient(uri, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=15000)
    info = client.admin.command('hello')
    print("✅ Connexion réussie !")
    print("ReplicaSet :", info.get('setName'))
except Exception as e:
    print(f"❌ Erreur : {e}")