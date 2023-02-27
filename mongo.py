import os
import pymongo
if os.path.exists("env.py"): 
    import env


MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "database0"
COLLECTION = "humans"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


conn = mongo_connect(MONGO_URI)

coll = conn[DATABASE][COLLECTION]

# Add insertion code here...
""" Insert single document
new_doc = {"first": "douglas", "last": "adams", "dob": "11/03/1952", "gender": "m", "hair_color": "grey", "occupation": "writer", "nationality": "british"}
coll.insert_one(new_doc) """

""" Insert multiple documents
new_docs = [{
    "first": "terry",
    "last": "pratchett",
    "dob": "28/04/1948",
    "gender": "m",
    "hair_color": "not much",
    "occupation": "writer",
    "nationality": "british"
}, {
    "first": "george",
    "last": "rr martin",
    "dob": "20/09/1948",
    "gender": "m",
    "hair_color": "white",
    "occupation": "writer",
    "nationality": "american"
}]
coll.insert_many(new_docs) """

# documents = coll.find({"first": "douglas"})
# coll.delete_one({"first": "douglas"})
coll.update_many({"nationality": "american"}, {"$set": {"hair_color": "maroon"}})
documents = coll.find({"nationality": "american"})

# documents = coll.find()

for doc in documents:
    print(doc)