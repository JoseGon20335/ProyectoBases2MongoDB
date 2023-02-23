from flask import Flask, render_template, request, redirect, url_for, flash
# from pymongo import MongoClient
from pymongo import MongoClient
import random
import logging
import urllib.parse
import pymongo
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

with open('C:\Users\josem\OneDrive\Documents\GitHub\ProyectoBases2MongoDB\movies.json') as f:
    print(f)
    data = json.load(f)

# Insert data into MongoDB
result = db.my_collection.insert_many(data)
print(f"Inserted {len(result.inserted_ids)} documents")
