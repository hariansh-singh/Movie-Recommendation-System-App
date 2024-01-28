import os
from flask import Flask, render_template, request
# import joblib
import gzip  
import pickle
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder=os.path.abspath('templates'), static_url_path='/images', static_folder='images')


# movies = pickle.load('movie_list.pkl')
# movies = pickle.load(open('movie_list.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))  

with gzip.open('movie_list.pkl.gz', 'rb') as f:
    movies = pickle.load(f)

# Load and decompress the similarity.pkl
with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)

TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
TMDB_BASE_URL = os.getenv('TMDB_BASE_URL','')


def recommend(movie):
    
    movie_lower = movie.lower()
    movies['title_lower'] = movies['title'].str.lower()
    movie_index1 = movies[movies['title_lower'] == movie_lower].index

    if not movie_index1.empty:
        movie_index1 = movie_index1[0]
        distances = similarity[movie_index1]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
    
        recommended_movies = [{'title': movies.iloc[i[0]].title, 'poster_path': get_movie_poster(movies.iloc[i[0]].movie_id)} for i in movies_list]
        return recommended_movies

def get_movie_poster(movie_id):
    try:
        url = f'{TMDB_BASE_URL}{movie_id}?api_key={TMDB_API_KEY}'
        response = requests.get(url)
        response.raise_for_status()  
        movie_details = response.json()
        poster_path = movie_details.get('poster_path')
        
        if poster_path:
            image_url = f'https://image.tmdb.org/t/p/w185{poster_path}'
            return image_url
        else:
            print(f"No poster available for movie {movie_id}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for movie {movie_id}: {e}")
        return None
        

@app.route('/') 
def index():
    user_input = request.args.get('movie_input', '')
    
    filtered_movies = [title for title in movies['title'] if user_input.lower() in title.lower()]

    suggestions = filtered_movies[:7]
    

    
    return render_template('index.html', movies=movies, suggestions=suggestions)

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    user_input = request.form.get('movie_input')

    recommended_movies = recommend(user_input)

    return render_template('recommendation.html', recommendations=recommended_movies)

if __name__ == '__main__':
    app.run(debug=True)


    
