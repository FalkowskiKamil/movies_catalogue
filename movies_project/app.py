from flask import Flask, render_template, url_for
import tmdb_client
from random import shuffle

app = Flask(__name__)

@app.route('/')
def homepage():
    movies = tmdb_client.get_movies(8)
    shuffle(movies)
    return render_template("homepage.html", movies=movies)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

if __name__ == '__main__':
    app.run(debug=True)