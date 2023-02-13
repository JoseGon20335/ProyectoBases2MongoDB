from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import random
import logging
import urllib.parse

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


@app.route("/")  # INDEX
def index():
    movies = db.movies
    moviesData = movies.find()

    return render_template(
        "index.html",
        moviesData=moviesData,
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
        "agregarPeliculaForm.html"
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


# UPDATE PRODUCTO
@app.route("/actualizarPeliculas/<String:Title>", methods=["GET", "POST"])
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


@app.route("/borrarPeliculaResul")  # PRE BORRAR PRODUCTO
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


@app.route("/borrarPelicula/<String:Title>")  # BORRAR PRODUCTO
def borrarPelicula(Title):
    movie = db.movies
    movie.delete_one({"Title": Title})
    flash("Pelicula borrada con éxito!")
    return redirect(url_for("borrarPeliculaResul"))


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


if __name__ == "__main__":
    app.run(debug=True)
