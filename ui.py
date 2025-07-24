import streamlit as st
import pickle
import pandas as pd
import requests
import os

st.title("🎬 Movie Recommendation System")

# Load the necessary files
with open("movie_data.pkl", "rb") as f:
    movie_data = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

with open("details.pkl", "rb") as f:
    details = pickle.load(f)

# Convert to DataFrame
movie_data = pd.DataFrame(movie_data)
similarity_data = pd.DataFrame(similarity)

# Use an environment variable for the API key
API_KEY = os.getenv("TMDB_API_KEY", "f11ca805ea8ddd941eef56ebb70dd032")

def fetch_poster(movie_id):
    """Fetches the movie poster from TMDb."""
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        )
        data = response.json()
        return f"https://image.tmdb.org/t/p/w185/{data.get('poster_path', '')}"
    except Exception:
        return "https://tse4.mm.bing.net/th?id=OIP.59acm7M8zfvbkDUNHr6KdQAAAA&pid=Api&P=0&h=220"

def recommender(movie, watched_movies):
    """Returns top 5 recommended movies with their details, excluding watched movies."""
    if movie in movie_data["title"].values:
        movie_index = movie_data[movie_data["title"] == movie].index.tolist()[0]
        distances = similarity_data[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:]
        
        movie_recommendations = []
        movie_posters = []
        overviews = []
        imdb = []
        genres = []
        cast = []
        director = []
        
        for i in movie_list:
            movie_title = movie_data.iloc[i[0]]["title"]
            if movie_title not in watched_movies:
                movie_id = movie_data.iloc[i[0]]["movie_id"]
                movie_recommendations.append(movie_title)
                overviews.append(details.iloc[i[0]]["overview"])
                imdb.append(details.iloc[i[0]]["vote_average"])
                genres.append(details.iloc[i[0]]["genres"])
                cast.append(details.iloc[i[0]]["cast"])
                director.append(details.iloc[i[0]]["crew"])
                movie_posters.append(fetch_poster(movie_id))
            if len(movie_recommendations) == 5:
                break
        
        return movie_recommendations, overviews, imdb, genres, cast, director, movie_posters
    else:
        st.error("🚨 Movie Not Found!")
        st.warning("Check the spelling or try another movie.")
        return [], [], [], [], [], [], []

# Movie selection UI
option = st.selectbox("🎥 Select a Movie", movie_data["title"].values)
watched_movies = st.multiselect("📌 Movies you've already watched", movie_data["title"].values, [])

# Show selected movie details immediately
if option in movie_data["title"].values:
    index = movie_data[movie_data["title"] == option].index[0]
    movie_id = movie_data.iloc[index]["movie_id"]
    poster_url = fetch_poster(movie_id)
    overview = details.iloc[index]["overview"]
    rating = details.iloc[index]["vote_average"]
    genre = details.iloc[index]["genres"]
    cast_list = details.iloc[index]["cast"]
    director_name = details.iloc[index]["crew"]

    st.subheader(f"🎞️ Selected Movie Details:")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(poster_url, use_container_width=True)
    with col2:
        st.markdown(f"**{option.title()}**")
        st.markdown(f"📝 **Description:** {overview}")
        st.markdown(f"⭐ **TMDb Rating:** `{rating}`")
        st.markdown(f"🎞️ **Genres:** {genre}")
        st.markdown(f"🎭 **Cast:** {cast_list}")
        st.markdown(f"🎥 **Director:** {director_name}")
    
    st.markdown("---")

# Recommendation trigger
if st.button("🎬 Recommend"): 
    similar_movies, overviews, imdb, genres, cast, director, posters = recommender(option, watched_movies)

    if similar_movies:
        st.subheader("📌 Recommended Movies")
        st.markdown("---")

        for i in range(len(similar_movies)):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(posters[i], use_container_width=True)
            with col2:
                st.markdown(f"**{similar_movies[i].title()}**")
                st.markdown(f"📝 **Description:** {overviews[i]}")
                st.markdown(f"⭐ **TMDb Rating:** `{imdb[i]}`")
                st.markdown(f"🎞️ **Genres:** {genres[i]}")
                st.markdown(f"🎭 **Cast:** {cast[i]}")
                st.markdown(f"🎥 **Director:** {director[i]}")
            st.markdown("---")
