from pymongo import MongoClient, InsertOne
import json


client = MongoClient(
    f"mongodb+srv://admin:123@cluster0.jholt4h.mongodb.net/?retryWrites=true&w=majority",
    socketTimeoutMS=30000,
)

try:
    # Checquear la conexion a la base de datos
    print(client.list_database_names())
except Exception as e:
    print("Error connecting to the database:", e)

db = client.get_database("moviesDB")

collection1 = db.movies
collection2 = db.series
collection3 = db.episodes

with open('C:\\Users\\josem\\OneDrive\\Documents\\GitHub\\ProyectoBases2MongoDB\\backup\\movies.json', encoding='utf-8') as f:
    print(f)
    data = json.load(f)

# Insert data into MongoDB
requests = [InsertOne(doc) for doc in data]
result = collection1.bulk_write(requests)

with open('C:\\Users\\josem\\OneDrive\\Documents\\GitHub\\ProyectoBases2MongoDB\\backup\\series.json', encoding='utf-8') as f:
    print(f)
    data = json.load(f)

# Insert data into MongoDB
requests = [InsertOne(doc) for doc in data]
result = collection2.bulk_write(requests)

with open('C:\\Users\\josem\\OneDrive\\Documents\\GitHub\\ProyectoBases2MongoDB\\backup\\episodes.json', encoding='utf-8') as f:
    print(f)
    data = json.load(f)

# Insert data into MongoDB
requests = [InsertOne(doc) for doc in data]
result = collection3.bulk_write(requests)
