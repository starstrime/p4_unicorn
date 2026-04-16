from pymongo.mongo_client import MongoClient

uri = "mongodb://Cluster17576:ZFhsTF5SZmZa@ac-cm2kdg3-shard-00-00.b6r6yys.mongodb.net:27017,ac-cm2kdg3-shard-00-01.b6r6yys.mongodb.net:27017,ac-cm2kdg3-shard-00-02.b6r6yys.mongodb.net:27017/?ssl=true&replicaSet=atlas-tl4q5z-shard-0&authSource=admin&appName=Cluster17576"
# Create a new client and connect to the server
client = MongoClient(uri)

def select_query(query_string, parameters=()):
    c = db.cursor()
    c.execute(query_string, parameters)
    out_array = []
    column_names = c.description
    for row in c.fetchall():
        item_dict = dict()
        for col in range(len(row)):
             item_dict.update({column_names[col][0]: row[col]})
        out_array.append(item_dict)
    c.close()
    db.commit()
    return out_array

def insert_query(table, data):
    c = db.cursor()
    placeholder = ["?"] * len(data)
    c.execute(f"INSERT INTO {table} {tuple(data.keys())} VALUES ({', '.join(placeholder)}) RETURNING *;", tuple(data.values()))
    row = c.fetchall()
    output = dict()
    for col in range(len(row[0])):
        output.update({c.description[col][0]: row[0][col]})
    c.close()
    db.commit()
    return output

def general_query(query_string, parameters=()):
    c = db.cursor()
    c.execute(query_string, parameters)
    c.close()
    db.commit()
