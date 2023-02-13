from flask import Flask, render_template, request, redirect, url_for, flash
# from pymongo import MongoClient
from pymongo import MongoClient
import random
import logging
import urllib.parse
import pymongo
import json

username = urllib.parse.quote_plus("Proyecto1")
password = urllib.parse.quote_plus("Proyecto1_02")

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

# open and read the JSON file
with open("data\movies.json") as file:
    data = json.load(file)

# use the bulk_write method to perform a bulk insert
bulk_insert = collection1.bulk_write(
    [pymongo.InsertOne(record) for record in data])
