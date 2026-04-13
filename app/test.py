from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://Cluster17576:ZFhsTF5SZmZa@ac-cm2kdg3-shard-00-00.b6r6yys.mongodb.net:27017,ac-cm2kdg3-shard-00-01.b6r6yys.mongodb.net:27017,ac-cm2kdg3-shard-00-02.b6r6yys.mongodb.net:27017/?ssl=true&replicaSet=atlas-tl4q5z-shard-0&authSource=admin&appName=Cluster17576"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
