from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://Cluster17576:ZFhsTF5SZmZa@ac-cm2kdg3-shard-00-00.b6r6yys.mongodb.net:27017,ac-cm2kdg3-shard-00-01.b6r6yys.mongodb.net:27017,ac-cm2kdg3-shard-00-02.b6r6yys.mongodb.net:27017/?ssl=true&replicaSet=atlas-tl4q5z-shard-0&authSource=admin&appName=Cluster17576"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

database = client["data"]
try:
    database.drop_collection("profiles")
finally: # always run regardless if dropped
    database.create_collection("profiles")
    database.profiles.create_index(["name"], unique=True, sparse=True)
    database.profiles.create_index(["password"], unique=True, sparse=True)
client.close()

# # PLACEHOLDER UNTIL MONGO WORKS
# c.executescript("""
#     DROP TABLE IF EXISTS profiles;
#     CREATE TABLE profiles (
#         username TEXT PRIMARY KEY,
#         password TEXT
#     );
# """)
#
# db.commit()
# db.close()
