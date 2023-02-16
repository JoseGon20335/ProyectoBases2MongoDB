from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import random
import logging
import urllib.parse
from bson.objectid import ObjectId

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
        update = {
            "$set": {
                "Title": Title,
                "Worldwide Gross": WorldwideGross,
                "US Gross": USGross,
                "Production Budget": ProductionBudget,
                "Release Date": ReleaseDate,
                "MPAA Rating": MPAARating,
                "Distributor": Distributor,
                "Director": Director,
                "IMDB Rating": IMDBRating,
                "IMDB Votes": IMDBVotes,
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
        inserts = {
            "Title": Title,
            "Worldwide Gross": WorldwideGross,
            "US Gross": USGross,
            "Production Budget": ProductionBudget,
            "Release Date": ReleaseDate,
            "MPAA Rating": MPAARating,
            "Distributor": Distributor,
            "Director": Director,
            "IMDB Rating": IMDBRating,
            "IMDB Votes": IMDBVotes,
        }
        movies.insert_one(inserts)
        return redirect(url_for("index"))
    return render_template(
        "agregar_pelicula.html"
    )


@app.route("/filtrar")
def filtrarTipo():
    return render_template(
        "filtrar.html"
    )


@app.route("/content/<int:page>")
def content(page):
    movies = db.movies

    products_per_page = 12
    total_products = movies.count_documents({})

    movies = (
        movies.find().skip((page - 1) * products_per_page).limit(products_per_page)
    )
    return render_template(
        "content.html",
        movies=movies,
        page=page,
        products_per_page=products_per_page,
        total_products=total_products,
    )


@app.route("/agregarPeliculaForm", methods=["GET", "POST"])
def agregarPeliculaForm():

    movies = db.movies
    moviesData = movies.find()

    random_id = random.randint(0, 100000000)

    while movies.find_one({"id": random_id}) is not None:
        random_id = random.randint(0, 100000000)

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
        inserts = {
            "id": random_id,
            "Title": Title,
            "Worldwide Gross": WorldwideGross,
            "US Gross": USGross,
            "Production Budget": ProductionBudget,
            "Release Date": ReleaseDate,
            "MPAA Rating": MPAARating,
            "Distributor": Distributor,
            "Director": Director,
            "IMDB Rating": IMDBRating,
            "IMDB Votes": IMDBVotes,
        }
        movies.insert_one(inserts)
        flash("Pelicula agregada con éxito!")
        return redirect(url_for("agregarPeliculaForm"))
    return render_template(
        "agregar_pelicula.html"
    )


@app.route("/actualizarPeliculaTitle")  # PRE UPDATE PRODUCTO
def actualizarPeliculaTitle():
    movies = db.movies
    moviesData = movies.find()
    query = request.args.get("q")
    if query:
        results = movies.find(
            {"Title": {"$regex": query, "$options": "i"}})
    else:
        results = []
    return render_template(
        "actualizarPeliculaTitle.html", query=query, results=results, movies=movies
    )


@app.route("/actualizarPeliculas/<Title>", methods=["GET", "POST"])
def actualizarPeliculas(Title):

    movies = db.movies
    movie = movies.find({"Title": Title})

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
        filter = {"Title": Title}
        update = {
            "$set": {
                "Title": Title,
                "Worldwide Gross": WorldwideGross,
                "US Gross": USGross,
                "Production Budget": ProductionBudget,
                "Release Date": ReleaseDate,
                "MPAA Rating": MPAARating,
                "Distributor": Distributor,
                "Director": Director,
                "IMDB Rating": IMDBRating,
                "IMDB Votes": IMDBVotes,
            }
        }
        movies.update_one(filter, update)
        flash("Pelicula actualizada con exito!")
    return render_template(
        "actualizarPeliculasForm.html",
        movie=movie,
    )


@app.route("/borrarPeliculaResul")
def borrarPeliculaResul():
    movies = db.movies

    moviesData = movies.find()
    query = request.args.get("q")
    if query:
        results = movies.find(
            {"Title": {"$regex": query, "$options": "i"}})
    else:
        results = []
    return render_template(
        "borrarPeliculaResul.html", query=query, results=results, moviesData=moviesData
    )


@app.route("/search")  # SEARCH BAR
def search():
    collection = db.movies
    query = request.args.get("q")
    if query:
        results = collection.find(
            {"Title": {"$regex": query, "$options": "i"}})
    else:
        results = []
    return render_template("search_results.html", query=query, results=results)



@app.route('/series_recommendations')
def series_recommendations():
    return render_template('series_recommendations.html')

@app.route('/series_results', methods=['POST'])
def series_results():
    selected_option = request.form['option']
    selected_field = request.form['field']
    
    if selected_option == 'rating':
        pipeline = [
            {'$group': {'_id': '$show_id', 'averageRating': {'$avg': '$rating'}}},
            {'$lookup': {'from': 'series', 'localField': '_id', 'foreignField': '_id', 'as': 'show'}},
            {'$unwind': '$show'},
            {'$project': {'_id': 0, 'title': '$show.title', 'averageRating': 1}},
            {'$sort': {'averageRating': -1}}
        ]
    elif selected_option == 'visualizations':
        pipeline = [
            {'$group': {'_id': '$show_id', 'averageVisualizations': {'$avg': '$visualizations'}}},
            {'$lookup': {'from': 'series', 'localField': '_id', 'foreignField': '_id', 'as': 'show'}},
            {'$unwind': '$show'},
            {'$project': {'_id': 0, 'title': '$show.title', 'averageVisualizations': 1}},
            {'$sort': {'averageVisualizations': -1}}
        ]
    elif selected_option == 'mpaa':
        pipeline = [
            {'$match': {'MPAA Rating': selected_field}},
            {'$group': {'_id': '$show_id', 'averageRating': {'$avg': '$rating'}}},
            {'$lookup': {'from': 'series', 'localField': '_id', 'foreignField': '_id', 'as': 'show'}},
            {'$unwind': '$show'},
            {'$project': {'_id': 0, 'title': '$show.title', 'averageRating': 1}},
            {'$sort': {'averageRating': -1}}
        ]
    
    results = list(episodes.aggregate(pipeline))
    
    return render_template('series_results.html', results=results)



if __name__ == "__main__":
    app.run(debug=True)


