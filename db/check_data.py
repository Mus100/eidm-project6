from pymongo import MongoClient

uri = "mongodb://admin_bio:g8OGNK8TUbz0I201@ac-rlvcorp-shard-00-00.nbj2m7f.mongodb.net:27017,ac-rlvcorp-shard-00-01.nbj2m7f.mongodb.net:27017,ac-rlvcorp-shard-00-02.nbj2m7f.mongodb.net:27017/?ssl=true&authSource=admin&replicaSet=atlas-mpwr7q-shard-0"

client = MongoClient(uri, tlsAllowInvalidCertificates=True)
col = client["biomedical_corpus"]["articles"]

for doc in col.find({}, {"title":1, "year":1, "domain":1, "_id":0}):
    print(doc)