from flask import Flask, render_template, request, url_for
import tmdb_client
from random import shuffle, choice
import random

app = Flask(__name__)

@app.route('/')
def homepage():
    movies_list=['now_playing', 'popular', 'top_rated', 'upcoming']
    selected_list=request.args.get('list_type', "popular")
    if selected_list not in movies_list:
        selected_list='popular'
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    shuffle(movies)
    return render_template("homepage.html", movies=movies, current_list=selected_list, movies_list=movies_list)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)[:10]
    movie_images = tmdb_client.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_images)
    selected_backdrop=selected_backdrop['file_path']
    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop)

if __name__ == '__main__':
    app.run(debug=True)
