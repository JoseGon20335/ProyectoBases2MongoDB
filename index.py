from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

app = Flask(__name__)
app.secret_key = "llave_secreta"

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
movies = db["movies"]
series = db["series"]
episodes = db["episodes"]


@app.route("/")
def index():
    movies = db.movies
    moviesData = movies.find()

    return render_template(
        "index.html",
        moviesData=moviesData,
    )


@app.route("/pelicula/<id>")
def pelicula(id):
    movies = db.movies
    movieData = movies.find_one({"_id": ObjectId(id)})

    return render_template(
        "pelicula_select.html",
        movieData=movieData,
    )


@app.route("/update_pelicula/<id>", methods=["GET", "POST"])
def updatePelicula(id):

    movies = db.movies
    movie = movies.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        Title = request.form.get("Title")
        WorldwideGross = request.form.get("Worldwide Gross")
        USGross = request.form.get("US Gross")
        ProductionBudget = request.form.get("Production Budget")
        ReleaseDate = request.form.get("Release Date")
        MPAARating = request.form.get("MPAA Rating")
        IMDBVotes = request.form.get("IMDB Votes")
        IMDBRating = request.form.get("IMDB Rating")
        Director = request.form.get("Director")
        Distributor = request.form.get("Distributor")
        MajorGenre = request.form.get("Major Genre")
        GenerosTxt = request.form.get("Generos")
        Generos = GenerosTxt.split(",")
        update = {
            "$set": {
                "Title": Title,
                "Worldwide Gross": WorldwideGross,
                "US Gross": USGross,
                "Major Genre": MajorGenre,
                "Production Budget": ProductionBudget,
                "Release Date": ReleaseDate,
                "MPAA Rating": MPAARating,
                "Distributor": Distributor,
                "Director": Director,
                "IMDB Rating": IMDBRating,
                "IMDB Votes": IMDBVotes,
                "Genres": Generos,
            }
        }
        movies.update_one({"_id": ObjectId(id)}, update)
        return redirect(url_for("index"))
    return render_template(
        "update_pelicula.html",
        movie=movie,
    )


@app.route("/borrar_pelicula/<id>")
def borrarPelicula(id):
    movie = db.movies
    movie.delete_one({"_id": ObjectId(id)})
    flash("Pelicula borrada con éxito!")
    return redirect(url_for("index"))


@app.route("/add_pelicula", methods=["GET", "POST"])
def addPelicula():

    movies = db.movies
    moviesData = movies.find()

    if request.method == "POST":
        Title = request.form.get("Title")
        WorldwideGross = request.form.get("Worldwide Gross")
        USGross = request.form.get("US Gross")
        ProductionBudget = request.form.get("Production Budget")
        ReleaseDate = request.form.get("Release Date")
        MPAARating = request.form.get("MPAA Rating")
        IMDBVotes = request.form.get("IMDB Votes")
        IMDBRating = request.form.get("IMDB Rating")
        Director = request.form.get("Director")
        Distributor = request.form.get("Distributor")
        MajorGenre = request.form.get("Major Genre")
        GenerosTxt = request.form.get("Generos")
        Generos = GenerosTxt.split(",")
        inserts = {
            "Title": Title,
            "Worldwide Gross": WorldwideGross,
            "US Gross": USGross,
            "Major Genre": MajorGenre,
            "Production Budget": ProductionBudget,
            "Release Date": ReleaseDate,
            "MPAA Rating": MPAARating,
            "Distributor": Distributor,
            "Director": Director,
            "IMDB Rating": IMDBRating,
            "IMDB Votes": IMDBVotes,
            "Genres": Generos,
        }
        movies.insert_one(inserts)
        return redirect(url_for("index"))
    return render_template(
        "agregar_pelicula.html"
    )


@app.route("/filtrar/<filtro>")
def filtrar(filtro):
    movies = db.movies
    if filtro == 'ratingGenre':
        return redirect(url_for("search_results_rating"))
    if filtro == 'titulo':  # listo
        return render_template(
            "search_results_titulo.html",
            filterName=filtro
        )
    if filtro == 'director':  # listo
        return render_template(
            "search_results_director.html",
            filterName=filtro
        )
    if filtro == 'distribuidor':  # listo
        return render_template(
            "search_results_distribuidor.html",
            filterName=filtro
        )
    if filtro == 'genre':  # listo
        return render_template(
            "search_results_genre.html",
            filterName=filtro
        )
    if filtro == 'mpaa':
        return render_template(
            "search_results_mpaa.html",
            filterName=filtro
        )

    results = movies.find()

    return render_template(
        "filtrar.html",
        filtro='none',
    )


@app.route("/search_results_mpaa")
def search_results_mpaa():
    movies = db.movies
    query = request.args.get("q")
    if query:
        results = movies.find(
            {"Title": {"$regex": query, "$options": "i"}})
    else:
        results = []
    return render_template("search_results_mpaa.html",
                           query=query,
                           results=results
                           )


@app.route("/search_results_titulo")
def search_results_titulo():
    movies = db.movies
    query = request.args.get("q")
    if query:
        results = movies.find(
            {"Title": {"$regex": query, "$options": "i"}})
    else:
        results = []
    return render_template("search_results_titulo.html",
                           query=query,
                           results=results
                           )

# Christopher Nolan


@app.route("/search_results_director")
def search_results_director():
    movies = db.movies
    query = request.args.get("q")
    if query:
        results = movies.find(
            {"Director": {"$regex": query, "$options": "i"}})
    else:
        results = []
    return render_template("search_results_director.html",
                           query=query,
                           results=results
                           )

# Lionsgate


@app.route("/search_results_distribuidor")
def search_results_distribuidor():
    movies = db.movies
    query = request.args.get("q")
    if query:
        results = movies.find(
            {"Distributor": {"$regex": query, "$options": "i"}})
    else:
        results = []
    return render_template("search_results_distribuidor.html",
                           query=query,
                           results=results
                           )

# Comedy
# Major Genre


@app.route("/search_results_genre")
def search_results_genre():
    movies = db.movies
    query = request.args.get("q")
    if query:
        results = movies.find(
            {"Major Genre": {"$regex": query, "$options": "i"}})
    else:
        results = []
    return render_template("search_results_genre.html",
                           query=query,
                           results=results
                           )


@app.route("/search_results_rating")
def search_results_rating():
    movies = db.movies
    query = request.args.get("q")
    if query:
        results = movies.find(
            {"Major Genre": {"$regex": query, "$options": "i"}})
        results = results.sort(
            [("IMDB Rating", -1)]).limit(10)

    else:
        results = movies.find().sort(
            [("IMDB Rating", -1)]).limit(10)
    return render_template("search_results_rating.html",
                           results=results
                           )


def bulk():
    db = client.get_database("moviesDB")

    collection = db.movies

    #with open('C:\Users\josem\OneDrive\Documents\GitHub\ProyectoBases2MongoDB\movies.json') as f:
    with open('./backup/movies_alpha.json') as f:
        print(f)
        data = json.load(f)

    # Insert data into MongoDB
    result = db.my_collection.insert_many(data)
    return redirect(url_for("index"))


@app.route('/series_recommendations', methods=["GET", "POST"])
def series_recommendations():
    selected_option = request.args.get('recommendation_type')
    selected_field = request.args.get('field')
    # series = db.series
    episodes = db.episodes
    if selected_option:
        if selected_option == 'rating':
            # db.episodes.aggregate([ {
            # $group: { _id: "$show_id", averageRating: { $avg: "$rating" } } }, {
            # $lookup: { from: "series", localField: "_id", foreignField: "_id", as: "show" } }, {
            # $unwind: "$show" }, {
            # $project: { _id: 0, title: "$show.title", averageRating: 1 } }, {
            # $sort: { averageRating: -1 } } ])

            pipeline = [
                {'$group': {'_id': '$show_id', 'averageRating': {'$avg': '$rating'}}},
                {'$lookup': {'from': 'series', 'localField': '_id',
                             'foreignField': '_id', 'as': 'show'}},
                {'$unwind': '$show'},
                {'$project': {'_id': 0, 'title': '$show.title', 'averageRating': 1}},
                {'$sort': {'averageRating': -1}}
            ]

        elif selected_option == 'visualizations':

            # db.episodes.aggregate([ {
            # $group: { _id: "$show_id", averageVisualizations: { $avg: "$visualizations" } } }, {
            # $lookup: { from: "series", localField: "_id", foreignField: "_id", as: "show" } }, {
            # $unwind: "$show" }, {
            # $project: { _id: 0, title: "$show.title", averageVisualizations: 1 } }, {
            # $sort: { averageVisualizations: -1 } } ])
            pipeline = [

                {'$group': {'_id': '$show_id', 'averageVisualizations': {
                    '$avg': '$visualizations'}}},
                {'$lookup': {'from': 'series', 'localField': '_id',
                             'foreignField': '_id', 'as': 'show'}},
                {'$unwind': '$show'},
                {'$project': {'_id': 0, 'title': '$show.title',
                              'averageVisualizations': 1}},
                {'$sort': {'averageVisualizations': -1}}
            ]

        elif selected_option == 'mpaa':

            pipeline = [
                {'$match': {'MPAA Rating': selected_field}},
                {'$group': {'_id': '$show_id', 'averageRating': {'$avg': '$rating'}}},
                {'$lookup': {'from': 'series', 'localField': '_id',
                             'foreignField': '_id', 'as': 'show'}},
                {'$unwind': '$show'},
                {'$project': {'_id': 0, 'title': '$show.title', 'averageRating': 1}},
                {'$sort': {'averageRating': -1}}
            ]
            pipeline = [
                {'$lookup': {'from': 'series', 'localField': 'show_id',
                             'foreignField': '_id', 'as': 'show'}},
                {'$unwind': '$show'},    {
                    '$match': {'show.rated': selected_field}},
                {'$group': {'_id': '$show_id', 'averageRating': {'$avg': '$rating'}}},
                {'$lookup': {'from': 'series', 'localField': '_id',
                             'foreignField': '_id', 'as': 'show'}},
                {'$unwind': '$show'},
                {'$project': {'_id': 0, 'title': '$show.title', 'averageRating': 1}},
                {'$sort': {'averageRating': -1}}

            ]

    else:
        pipeline = [
            {'$group': {'_id': '$show_id', 'averageRating': {'$avg': '$rating'}}},
            {'$lookup': {'from': 'series', 'localField': '_id',
                         'foreignField': '_id', 'as': 'show'}},
            {'$unwind': '$show'},
            {'$project': {'_id': 0, 'title': '$show.title', 'averageRating': 1}},
            {'$sort': {'averageRating': -1}}

        ]

    results = list(episodes.aggregate(pipeline))

    if len(results) == 0:
        print("No results found")

    # print(results)

    return render_template('series_recommendations.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
